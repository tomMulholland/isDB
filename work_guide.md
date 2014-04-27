PROJECT WORK FLOW
=================


#######################
# WORK PLAN

1. Get positive examples (done), unknown examples (done), and negative examples (done?)

2. Create table with all id, all text, and is_scholarship(boolean)

3. Label known scholarships as true, negative examples as false

3. Add features to schol_features:
   - Number of mentions of each word in schol_dict words
   - Number of total mentions of schol_dict words
     
4. Add features to schol_text_features
   - three words before and after
   - three words before
   - three words after
   - three words before contains person name?

4. Write default inference rule (features used to predict is_scholarship)

5. Other inference rules?

6. Adjust learning rate?

7. Add features to is_scholarship_requirement to predict which sentences contain relevant requirement data

8. Use existing scholarships to provide positive examples of requirement feature metadata

# TODO
## Get more negative examples. Consider financial aid pages from universities


#######################
# SCHOLARSHIP DICTIONARY
## This dictionary has grown and is available in scripts/scholarship_words.txt
eligible, requirement, apply, conditions, semester, quarter, visa, J-1, J1, F-1, F1, admit, accept, award, scholarship, college, university, foundation, international, country, student, graduate, MSc, M.Sc., PhD, Ph.D., deadline
TOEFL, PBT, CBT, IBT, IELTS
SAT, GRE, PSAT, AP, 

#COUNTRY DICTIONARY
<list all countries> <include disambiguations (UK, U.K., United Kingdom)

#DICTIONARY OF MAJORS
<Engineering, Law, etc.>

#######################
# CREATE DB
createdb isDB

#Modify the env.sh file with your database name:
#export DBNAME=isDB

# To reset isDB
psql -d isDB -c "DROP SCHEMA public CASCADE;"
psql -d isDB -c "CREATE SCHEMA public;"

# Load both data sets
psql -d isDB -c "CREATE TABLE scholarships( id bigserial primary key, text text);"
psql -d isDB -c "CREATE TABLE websites( id bigserial primary key, text text);"
psql -d isDB -c "CREATE TABLE financial_aid( id bigserial primary key, text text);"
psql -d isDB -c "CREATE TABLE schol_int_study( id bigserial primary key, text text);"

psql -d isDB -c "COPY scholarships FROM STDIN CSV;" < data/scholarships.csv
psql -d isDB -c "COPY websites FROM STDIN CSV;" < data/link_to.csv
psql -d isDB -c "COPY financial_aid FROM STDIN CSV;" < data/financial_aid.csv
psql -d isDB -c "COPY schol_int_study FROM STDIN CSV;" < data/schol_int_study.csv

psql -d isDB -c "ALTER TABLE scholarships ADD is_scholarship boolean"
psql -d isDB -c "UPDATE scholarships SET is_scholarship = TRUE"

psql -d isDB -c "ALTER TABLE financial_aid ADD is_scholarship boolean"
psql -d isDB -c "UPDATE financial_aid SET is_scholarship = FALSE"

psql -d isDB -c "ALTER TABLE websites ADD is_scholarship boolean"
psql -d isDB -c "ALTER TABLE schol_int_study ADD is_scholarship boolean"
psql -d isDB -c "INSERT INTO scholarships SELECT * FROM websites;" 
psql -d isDB -c "INSERT INTO scholarships SELECT * FROM financial_aid;"
psql -d isDB -c "INSERT INTO scholarships SELECT * FROM schol_int_study;"


#####################
# COMPILE NATURAL LANGUAGE PROCESSOR
## Not using this
cd deepdive/app/isDB/udf/nlp_extractor
sbt stage

######################
# CREATE AND POPULATE SENTENCE TABLES
## NLP NO LONGER IN USE
#########################################
# NO NATURAL LANGUAGE PROCESSING
## NLP did very badly on these texts at recognizing "ORGANIZATION"
# SKIP THIS SECTION
psql -d isDB -c "CREATE TABLE schol_sentences(
  id bigserial primary key, 
  document_id bigint,
  sentence text, 
  words text[],
  lemma text[],
  pos_tags text[],
  dependencies text[],
  ner_tags text[]);"

psql -d isDB -c "CREATE TABLE web_sentences(
  id bigserial primary key,
  document_id bigint,
  sentence text, 
  words text[],
  lemma text[],
  pos_tags text[],
  dependencies text[],
  ner_tags text[]);"

#in application.conf
    ext_sentences.input: """SELECT id as "schol_id", text as "schol_text" FROM scholarships order by id asc"""
    ext_sentences.output_relation: "schol_sentences"
    ext_sentences.udf: ${APP_HOME}"/udf/nlp_extractor/run.sh -k schol_id -v schol_text -l 20"
    ext_sentences.before: ${APP_HOME}"/udf/before_schol_sentences.sh"

    ext_sentences.input: """SELECT id as "web_id", text as "web_text" FROM websites order by id asc"""
    ext_sentences.output_relation: "web_sentences"
    ext_sentences.udf: ${APP_HOME}"/udf/nlp_extractor/run.sh -k web_id -v web_text -l 20"
    ext_sentences.before: ${APP_HOME}"/udf/before_web_sentences.sh"


##in before_schol_sentences.sh
#! /usr/bin/env bash
psql -c "TRUNCATE schol_sentences CASCADE;" isDB
psql -c "TRUNCATE web_sentences CASCADE;" isDB

##in before_web_sentences.sh
#! /usr/bin/env bash
psql -c "TRUNCATE web_sentences CASCADE;" isDB

## Parsing of schol_text:
[success] Total time: 5408 s, completed Apr 18, 2014 7:56:20 PM
##Parsing of web_text:
takes ~10 minutes
##schol_text sentence table = 10MB
##web_text sentence table = 16 MB
##What??
## Sentences were very big (run-ons) because there were no periods "." After adding these, the run time for schol_sentences was reduced
[success] Total time: 444 s, completed Apr 19, 2014 11:58:51 AM


psql -d isDB -c "\COPY schol_sentences to '/home/tom/deepdive/app/isDB/data/schol_sentences_dump.csv' delimiter ',' csv header;"
psql -d isDB -c "\COPY web_sentences to '/home/tom/deepdive/app/isDB/data/web_sentences_dump.csv' delimiter ',' csv header;"


####################################
## EXTRACT FEATURES FROM SCHOLARSHIP WORDS

psql -d isDB -c "CREATE TABLE schol_features(
  id bigserial primary key, 
  text_id bigint references scholarships(id),
  feature text);"


    ext_schol.input: "SELECT * FROM scholarships"
    ext_schol.output_relation: "schol_features"
    ext_schol.udf: ${APP_HOME}"/scripts/extract_dictionary_mentions.py"
    ext_schol.before: ${APP_HOME}"/udf/before_schol_features.sh"

#before_schol_features.sh
#! /usr/bin/env bash
psql -c "TRUNCATE schol_features CASCADE;" isDB

##########################################
## WEIRD PROBLEM
Deepdive doesn't like it when I include parallel python (pp) workers in extract_dictionary_mentions.py, but text processing would be much better parallelized.

###########################################
## INFERENCE FACTORS

inference.factors {
  f_is_schol_features.input_query: """
    SELECT scholarships.id as "scholarships.id", scholarships.is_scholarship, feature 
    FROM scholarships, schol_features
    WHERE scholarships.id = schol_features.text_id"""
  f_is_schol_features.function: "IsTrue(scholarships.is_scholarship)"
  f_is_schol_features.weight: "?(feature)"
}
schema.variables {
    scholarships.is_scholarship: Boolean
  }

  pipeline.pipelines.nonlp: ["ext_schol", "f_is_schol_features"]

#############################################
## SAMPLER
calibration.holdout_fraction: 0.20
sampler.sampler_args: "-l 125 -s 1 -i 200 --alpha 0.001"

## Haven't tested this
ALTER TABLE web_sentences ADD COLUMN id_orig numeric;
UPDATE TABLE web_sentences SET id_orig = (SELECT websites.id_orig
  FROM websites, web_sentences
  WHERE websites.id = web_sentences.id);


