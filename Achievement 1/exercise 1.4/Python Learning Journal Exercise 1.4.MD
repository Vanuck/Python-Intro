# Python for Web Developers Learning Journal

## Exercise 1.4: File Handling in Python

## Reflection Questions

### 1. Why is file storage important when you’re using Python? What would happen if you didn’t store local files?

- As well as reading and writing files, Python can manipulate them. You need to know what files are on the file system and sometimes you need to delete them too. Data would be lost when the program ends if you couldn't store local files.

### 2. In this Exercise you learned about the pickling process with the pickle.dump() method. What are pickles? In which situations would you choose to use pickles and why?

- Pickle in Python is primarily used in serializing and deserializing a Python object structure.
- The Pickle module is a great resource when you want to store and reuse objects. For example, the functions dump() and load() help serialize/deserialize objects. Dumps() and loads() handle that same process for memory instead of external storage.

### 3. In Python, what function do you use to find out which directory you’re currently in? What if you wanted to change your current working directory?

- os.getcwd() is used to find out the current working directory.
- os.chdir(path) is used to change the current working directory

### 4. Imagine you’re working on a Python script and are worried there may be an error in a block of code. How would you approach the situation to prevent the entire script from terminating due to an error?

- You would use try-except blocks.

### 5. You’re now more than halfway through Achievement 1! Take a moment to reflect on your learning in the course so far. How is it going? What’s something you’re proud of so far? Is there something you’re struggling with? What do you need more practice with? Feel free to use these notes to guide your next mentor call.

- So far the learing is going smoothly. Will be practicing more with operators and functions, as that area is still weak for me I feel. I am happy with the results of each exercise so for in this Python Module.
