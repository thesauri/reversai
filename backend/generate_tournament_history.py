import random

teams = ['Pikachu', 'Squirtle', 'Dratini', 'Meowth', 'Psyduck', 'Charmander', 'Bulbasaur', 'Eevee']
groups = [teams[0:4], teams[4:8]]
games = []

for _ in range(3):
  for group in groups:
    for i in range(len(group)):
      for j in range(i + 1, len(group)):
        player1_points = random.randint(10, 50)
        player2_points = 64 - player1_points
        games.append(
          {
            'white': {
              'score': player1_points,
              'name': group[i]
            }, 
            'black': {
              'score': player2_points,
              'name': group[j]
          }})

print(games)
print(groups)