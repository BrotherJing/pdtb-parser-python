### Parserhelper

This small tool is a wrapper for Stanford Parser. It is used to generate parse tree and dependency tree for every sentence in the original training data. Each time it reads one line(a json object) from the input file, and output one line with a json object with parse tree and dependency tree.
The format of input and output json is
```
#input
{
	"Sense":[],
	"Arg1":{
		"Word":[],
		"RawText":"..."
	},
	"Arg2":{
		"Word":[],
		"RawText":"..."
	},
	"ID":"..."
}

#output
{
	"Sense":[],
	"Arg1":{
		"Word":[],
		"ParseTree":"...",
		"Dependency";[]
	},
	"Arg2":{
		"Word":[],
		"ParseTree":"...",
		"Dependency";[]
	},
	"ID":"..."
}
```

### Usage
```
java -jar parserhelper.jar <input file> <output file>
```