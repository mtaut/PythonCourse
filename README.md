# RecipeApp (Command Line Version)
This is the command line version of a recipe app, which acts as a precursor to its web app counterpart.

## Context
This project focuses on Python fundamentals, data structures, and object-oriented programming. The project also utilizes a database with MySQL and builds the foundation for interacting with a Django framework, for a later project. 

## User Goals
Users will be able to create and modify recipes with ingredients, add cooking times, search for a recipe by ingredient, and delete a recipe. A difficulty parameter will also be part of the app that is automatically calculated within the app.

## Features
- **Create and manage the user's recipes on a locally hosted MySQL database**
- **Option to search for recipes that contain a set of ingredients specified by the user**
- **Automatically rate each recipe by their difficulty level**
- **Display more details on each recipe if the user prompts it, such as the ingredients, cooking time, and difficulty of the recipe**

## Technical Requirements
- **App should handle any common exceptions or errors that may pop up either during user input, database access, and display user-friendly error messages.**
- **App must connect to a MySQL database hosted locally on system.**
- **App must provide an easy to use interface, supported by simple forms of input and concise instructions that any user can follow.**
- **App should work on Python3.6+ installations.**

## Installation
1. Clone the repository: `git clone <repository_url>`
2. Navigate to the project directory: `cd recipe_app`
3. Install required packages: `pip install -r requirements.txt`
4. Configure the MySQL database:
   - Create a database
   - Create 'Recipes' table

## Usage
1. Run the application: 'python recipe_app'
2. Follow on-screen prompts to:
   - Add a new recipe
   - Search for recipe by ingredient
   - View, update, or delete recipe



