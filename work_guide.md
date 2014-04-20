PROJECT WORK FLOW
=================


#######################
# WORK PLAN

1. DO NOT (Perform natural language processing on raw text)
   Perform natural language processing on raw text

2. Extract mentions of schol_dict words
   (Extract mentions of people in the text)

3. 
   (Extract all pairs of people that possibly participate in a has_spouse relation)

4. Add features to is_scholarship to predict which texts are scholarships
   (Add features to our has_spouse candidates to predict which ones are correct or incorrect)

5. Use existing scholarships to provide positive examples of feature metadata
   (Write inference rules to incorporate domain knowledge that improves our predictions)

6. Add features to is_scholarship_requirement to predict which sentences contain relevant data

7. Use existing scholarships to provide positive examples of requirement feature metadata

# TODO
## Get more negative examples. Consider financial aid pages from universities


#######################
# SCHOLARSHIP DICTIONARY

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

#Load both data sets
psql -d isDB -c "CREATE TABLE scholarships( id bigserial primary key, text text);"
psql -d isDB -c "CREATE TABLE websites( id bigserial primary key, text text);"

psql -d isDB -c "copy scholarships from STDIN CSV;" < data/scholarships.csv
psql -d isDB -c "copy websites from STDIN CSV;" < data/link_to.csv


#####################
# COMPILE NATURAL LANGUAGE PROCESSOR
cd deepdive/app/isDB/udf/nlp_extractor
sbt stage

######################
# CREATE AND POPULATE SENTENCE TABLES
## NLP NO LONGER IN USE
#########################################
# NO NATURAL LANGUAGE PROCESSING
## NLP did very badly on these texts at recognizing "ORGANIZATION"
### GO TO NEXT SECTION
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
## EXTRACT MENTIONS OF SCHOLARSHIP WORDS

psql -d isDB -c "CREATE TABLE schol_mentions(
  id bigserial primary key, 
  sentence_id bigint references schol_sentences(id),
  start_position int,
  length int,
  text text);"

psql -d isDB -c "CREATE TABLE web_mentions(
  id bigserial primary key, 
  sentence_id bigint references web_sentences(id),
  start_position int,
  length int,
  text text);"

    ext_schol.input: "SELECT * FROM web_sentences"
    ext_schol.output_relation: "web_mentions"
    ext_schol.udf: ${APP_HOME}"/scripts/get_json_from_deepdive.py"
    ext_schol.before: ${APP_HOME}"/udf/before_web.sh"
    ext_schol.dependencies: ["ext_sentences"]






## Haven't tested this
ALTER TABLE web_sentences ADD COLUMN id_orig numeric;
UPDATE TABLE web_sentences SET id_orig = (SELECT websites.id_orig
  FROM websites, web_sentences
  WHERE websites.id = web_sentences.id);


