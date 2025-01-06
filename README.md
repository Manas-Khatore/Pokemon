# Pokemon

This repo is a working collection of personal projects relating to Pokemon data. A description of each project and the corresponding files can be found below:

## Project 1: Pokemon Type Matchups

In this project, I convert tabular data on Pokemon types into a graphical representation and use that to visualize each Pokemon's weaknesses and resistances. The main goals of this project are:
- Visualize Pokemon type relationships as a network graph (done)
- Allow users to input a Pokemon name, returns a network graph displaying weaknesses and resistances (done)
- Determine the primary weaknesses of a given team and suggest moves to counter those (in progress)
- **Tools used:** NetworkX, FastAPI, Python

Files:
- pk_types.ipynb: experimentation on network graph visualization
- pk_types.py: functions used to calculate weaknesses and resistances for specific Pokemon, called in main.py
- main.py: code for API

<img width="1044" alt="Screenshot 2025-01-06 at 12 19 16 AM" src="https://github.com/user-attachments/assets/8fced02f-0e26-46d4-add2-8bc5d09e02bf" />

