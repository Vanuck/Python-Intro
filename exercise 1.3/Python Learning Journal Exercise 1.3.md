# Python for Web Developers Learning Journal

## Exercise 1.2: Operators and Functions in Python

## Reflection Questions

### 1. In this Exercise, you learned how to use if-elif-else statements to run different tasks based on conditions that you define. Now practice that skill by writing a script for a simple travel app using an if-elif-else statement for the following situation:

- The script should ask the user where they want to travel.
- The user’s input should be checked for 3 different travel destinations that you define.
- If the user’s input is one of those 3 destinations, the following statement should be printed: “Enjoy your stay in **\_\_**!”
- If the user’s input is something other than the defined destinations, the following statement should be printed: “Oops, that destination is not currently available.”
- Write your script here. (Hint: remember what you learned about indents!)

destination=input(Where do you want to travel?")

if destination == "Mexico":
print("Have a great time in Mexico!")
elif destination == "Bermuda":
print("Have a great time in Bermuda!")
elif destination == "London":
print("Have a great time in London!")
else:
print("Oops, that destination is not currently available.”)

### 2. Imagine you’re at a job interview for a Python developer role. The interviewer says “Explain logical operators in Python”. Draft how you would respond.

- Just like arithmetic operators like +, -, \* and /, Python also supports comparison operators such as <, >, <=, >=, ==, and !=. These operators are often used to compare values: for example, if you'd like to check whether the number of items in your shopping cart (stored into a variable called items) is greater than 15, you use the expression items > 15 in Python, returning a value of True, or False.
  As well to check multiple conditions at the same time Python supports Boolean Logic Operators. Example operators supported are: and, or, not, if-else, & elif.

### 3. What are functions in Python? When and why are they useful?

- A function is a block of code which only runs when it is called. You can pass data, known as parameters, into a function. A function can return data as a result. They are useful becuase once written they can be used in multiple places.

### 4. In the section for Exercise 1 in this Learning Journal, you were asked in question 3 to set some goals for yourself while you complete this course. In preparation for your next mentor call, make some notes on how you’ve progressed towards your goals so far.

- I feel I am progessing on the 3 goals I set.
  1: I am getting to know Python
  2: I better understand Python and be able to use its powerful automation and scripting capabilities.
  3: My Python and programming confidence is going up.
