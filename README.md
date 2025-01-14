# Pokemon

<img width="1465" alt="Screenshot 2025-01-13 at 10 38 38 PM" src="https://github.com/user-attachments/assets/d27826c4-1ad2-487b-81c1-ed76a870d058" />

This repo is a working collection of personal projects relating to Pokemon data. A description of each project and the corresponding files can be found below:

## Project 1: Pokemon Type Matchups

In this project, I convert tabular data on Pokemon types into a graphical representation and use that to visualize each Pokemon's weaknesses and resistances. Users can interact with this through the typegraph function in the FastAPI deployment. The main goals of this project are:
- Visualize Pokemon type relationships as a network graph (done)
- Allow users to input a Pokemon name, returns a network graph displaying weaknesses and resistances (done)
- Determine the primary weaknesses of a given team and suggest moves to counter those (in progress)
- **Tools used:** NetworkX, FastAPI, Python

Files:
- pk_types.ipynb: experimentation on network graph visualization
- pk_types.py: functions used to calculate weaknesses and resistances for specific Pokemon, called in main.py
- main.py: code for API

<img width="1044" alt="Screenshot 2025-01-06 at 12 19 16 AM" src="https://github.com/user-attachments/assets/8fced02f-0e26-46d4-add2-8bc5d09e02bf" />

## Project 2: Pokemon Team Statistics and Move Recommendations

While knowing an individual Pokemon's weaknesses and resistances can be useful, players are often concerned about the overall weaknesses of their team to make sure it's well-balanced. The teamstats function allows users to enter a team of up to 6 Pokemon and retrieve the top 3 weaknesses of their team, according to the number of their Pokemon that are weak to each type. This is done using the earlier network graph data on Pokemon type relationships. Additionally, players can use the newmoves function to suggest moves that their team can learn to counter their top 3 weaknesses. Moves are suggested for Pokemon on their team that are NOT weak to each type. For this function, I used PostgreSQL to clean and store the data, integrating with my Python code using the psycopg2 package.

Files:
- pk_types.py: functions used for teamstats
- battle_recommend.py: functions used for newmoves
- all SQL files used for Pokemon move data
- **Tools used:** NetworkX, FastAPI, PostgreSQL, Python

<img width="1411" alt="Screenshot 2025-01-13 at 10 48 58 PM" src="https://github.com/user-attachments/assets/f103c87b-4d7d-46c1-bb1b-f6b89b1f1ea8" />

<img width="698" alt="Screenshot 2025-01-13 at 10 49 47 PM" src="https://github.com/user-attachments/assets/deae841e-ee1f-4823-a33e-b57569694df2" />


