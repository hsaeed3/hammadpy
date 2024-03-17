from hammadml.data import Database, VectorDatabase
from hammadml.text import CrossEncoder
from hammadml.llms import Instructor 
# OR from hammadml.llms import Anthropic

# UNCOMMENT IF YOU GET "Can't find model 'en_core_web_sm'..."
# from spacy.cli import download
# download("en_core_web_sm")

# Building Databases (Uses Example Documents from /tutorials/docs)
db = Database()
db.load_docs(dir="docs") # Generates a new database
vectordb = VectorDatabase()
vectordb.create_from_database("databases/db")

# PreProcessing Query (Retrieval)
query = "Who is tow mater?"
encoder = CrossEncoder()
db_results = db.search(query=query)
vectordb_results = vectordb.search(query=query)
ranked_results = encoder.rank(query=query, x=db_results, y=vectordb_results)

# Preparing LLM (Augmentation)
system_prompt = f"""# CONTEXT
You are a master of speaking organically and naturally. You have just searched your memory, and returned this
relevant information to use: This information is based on the user's query and the retrieved information, You will never
use this information as a first person, or as a direct quote. You will always paraphrase and use your own style to convey
the message.
<BEGIN CONTEXT>
{[sentence for sentence in ranked_results]}
<END CONTEXT>

# OBJECTIVE
Using the retrieved information defined above, you will answer the user's query in an incredibly skillfull manner.
You can paraphrase, quote, etc. as long as the information is relevant and accurate. Do not just directly copy and paste,
the information. You must use your own words and style to convey the information. Your response style must be friendly;
first iterating that you have found the information, and then providing an answer to the user's query; that implements the 
retrieved information, in a skillfull manner.
"""

# Query LLM (Generation)
llm = Instructor() # If key is blank, the OPENAI_API_KEY environment variable will be used.
# You can use llm = Instructor(api_key="YOUR_API_KEY") as well
completion = llm.instruct(system=system_prompt, query=query, model="4")
print("")
print("Database Results:")
print(db_results)
print("")
print("Vector Database Results:")
print(vectordb_results)
print("")
print("Cross Encoder Results:")
print(ranked_results)
print("")
print("LLM Completion:")
print(completion)