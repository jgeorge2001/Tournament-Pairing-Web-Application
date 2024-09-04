from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setup_teams', methods=['POST'])
def setup_teams():
    num_teams = int(request.form['num_teams'])
    if num_teams % 2 != 0:
        return "Please enter an even number of teams."

    return render_template('teams.html', num_teams=num_teams)

@app.route('/generate_tournament', methods=['POST'])
def generate_tournament():
    num_teams = int(request.form.get('num_teams', 0))
    if num_teams == 0:
        return "No number of teams specified or invalid number."

    teams = []
    for i in range(1, num_teams + 1):
        team_name = request.form.get(f'team_{i}_name')
        team_wins = request.form.get(f'team_{i}_wins')
        if team_name and team_wins:
            teams.append({'name': team_name, 'wins': int(team_wins)})

    teams = sorted(teams, key=lambda x: x['wins'])
    pairings = []

    while len(teams) >= 2:
        min_team = teams.pop(0)
        max_team = teams.pop(-1)
        pairings.append((max_team, min_team))

    return render_template('pairings.html', pairings=pairings)

if __name__ == '__main__':
    app.run(debug=True)
