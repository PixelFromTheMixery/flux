Doc String Snippets

``` JSON
{
	"Python Method Docstring": {
		"prefix": "pydoc",
		"body": [
			"\"\"\"",
			"${1:Summary of the function.}",
			"",
			"Args:",
			"    ${2:arg1} (${3:type}): ${4:Description of arg1.}",
			"    ${5:arg2} (${6:type}): ${7:Description of arg2.}",
			"    ${8:arg3} (${9:type}): ${10:Description of arg3.}",
			"",
			"Returns:",
			"    ${11:type}: ${12:Description of return value.}",
			"Raises:",
			"    ${13:Exception}: ${14:Conditions.}",
			"\"\"\"",
			"$0"
		],
		"description": "Custom Google-style method docstring"
	},
	"Python Class Docstring": {
		"prefix": "pydocclass",
		"body": [
			"\"\"\"",
			"${1:Summary of Class.}",
			"",
			"Attributes:",
			"    ${2:att1} (${3:type}): ${4:Description of att1.}",
			"    ${5:att2} (${6:type}): ${7:Description of att2.}",
			"    ${8:att3} (${9:type}): ${10:Description of att3.}",
			"",
			"Methods:",
			"    ${11:meth1}: ${12:Description of meth1}",
			"    ${13:meth2}: ${14:Description of meth2}",
			"    ${15:meth3}: ${16:Description of meth3}",
			"\"\"\"",
			"$0",
		],
		"description": "Custom Google-style class docstring"
	},
	"Python Module Docstring": {
		"prefix": "pydocmodule",
		"body": [
			"\"\"\"",
			"${1:Brief description of the module.}",
			"",
			"${2:Detailed explanation of the module's purpose and functionality.}",
			"",
			"Attributes:",
			"    ${3:variable} (${4:type}): ${5:Description of a module-level variable.}",
			"",
			"Classes:",
			"    ${6:class}: ${7:Description of a module-level class.}",
			"",
			"Methods:",
			"    ${8:method}: ${9:Description of a module-level method.}",
			"",
			"TODO: ${10:Upcoming task or fix.}",
			"\"\"\"",
			"$0"
		],
		"description": "Custom Google-style method docstring"
	}
}
```