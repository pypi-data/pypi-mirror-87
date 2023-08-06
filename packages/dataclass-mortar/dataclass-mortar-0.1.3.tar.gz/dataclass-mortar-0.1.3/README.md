# mortar

naturally use dataclasses with Alchemy 

Experimental concept for easying the use of Dataclasses with Alchemy. Simple models and relationships work, anything more complicated probly won't. 

## Usage
Decorate a dataclass with `@persist` 
Column definitions are automatically generated based off the field data, relationships are created for any field that had a type of another dataclass. Column definitions can be passed to mortar via the metadata attribute of the field() method (provided by dataclass). Partial Column data can also be passed any other required fields of the column will be generated based off the field definition. 


## Primary Keys
mortar will try to find the proper primary key for a defined class. It will evaluate the columns in this order to find a primary key: 
1. Checks for predefined key via A partial column definition  `Column(primary_key=True)` 
1. Check for a column named <class_name.lower()>_id 
1. check for an id column name 
1. create and auto increment column designated as primary key