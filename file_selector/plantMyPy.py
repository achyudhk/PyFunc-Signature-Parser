
import sys
from fileRetriever import Retriever
from varExtractor import Extractor
def makeComment(struct):
	comments = {}
	for path,files in struct.items():
		print(path)
		comments[path] = []
		for funcs in files:
			#print ("method name: " + funcs['name'])
			mypy_str = "# type: ( "

			if len(funcs['params']) > 0:
				for params in  funcs['params']:
					#print (params)
					mypy_str += get_mypy_type(params[1]) + ', ' 
					#print ("param: " + params)
				mypy_str = mypy_str[:-2]
			mypy_str += ') -> '
			if len(funcs['returns']) > 0:
				for returns in funcs['returns']:
					mypy_str += get_mypy_type(returns[1]) + ', ' 
					#print ("return: " + returns)
				mypy_str = mypy_str[:-2]
			else:
				mypy_str += 'None'

			print (funcs['name'])
			print( mypy_str)
			comments[path].append({'method' : funcs['name'], 'line' : funcs['line'], 'comment': mypy_str})
			print ("***")
	print(comments)
	return comments

def get_mypy_type(string):
	if 'str' in string.lower():
		return 'str'
	elif 'int' in string.lower():
		return 'int'
	elif 'float' in string.lower() :
		return 'float'
	elif 'array' in string.lower() :
		return 'List'
	elif 'boolean' in string.lower():
		return 'bool'
	elif 'dict' in string.lower():
		return 'Tuple'
	else:
		return 'None'

def plantComments(comments):
	for item, value in comments.items():
		f = open(item, 'r')
		contents = f.readlines()
		f.close()
		for comment in value:
		#contents.insert(item['line']-1, item['comment'])
			line = contents[comment['line']-1][:-2]
			line = line + " " + comment['comment'] + "\n"
			contents[comment['line']-1] = line

		f2 = open(item+'_', 'w')
		contents = "".join(contents)
		f2.write(contents)
		f2.close()
		#print (contents)
		#print ("_____")


if __name__ == "__main__":
    retriever = Retriever()
    if(len(sys.argv) < 2):
        raise Exception("Usage: python plantMyPy.py <path\\to\\root\\directory>")
    root_folder = sys.argv[1]
    py_files = retriever.list_all_files_in_folder(root_folder)

    output_json = {}

    for py_file in py_files:
        declarations = Extractor.get_declarations(py_file)
        output_json[py_file] = declarations
    #print (output_json)
    comments = makeComment(output_json)
    plantComments(comments)

	
