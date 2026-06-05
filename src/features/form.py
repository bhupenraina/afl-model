import pandas as pd

df = pd.read_csv("data/cleaned/team_stats.csv", low_memory = False)

df = df.sort_values('match_date')

team_stat_cols = ['kicks', 'marks', 'handballs', 'disposals', 'effective_disposals','hitouts', 'tackles', 'rebounds', 'inside_fifties', 'clearances', 'clangers', 'free_kicks_for', 'free_kicks_against','contested_possessions', 'uncontested_possessions', 'contested_marks', 'marks_inside_fifty', 'one_percenters', 'bounces', 'goal_assists','afl_fantasy_score', 'supercoach_score', 'centre_clearances', 'stoppage_clearances', 'score_involvements', 'metres_gained', 'turnovers', 'intercepts', 'tackles_inside_fifty', 'contest_def_losses', 'contest_def_one_on_ones', 'contest_off_one_on_ones', 'contest_off_wins', 'def_half_pressure_acts', 'effective_kicks', 'f50_ground_ball_gets', 'ground_ball_gets', 'hitouts_to_advantage','intercept_marks', 'marks_on_lead', 'pressure_acts', 'rating_points', 'ruck_contests', 'score_launches', 'shots_at_goal', 'spoils']

rolling_stats = df.groupby('player_team')[team_stat_cols].transform(lambda x: x.shift(1).rolling(5).mean())

rolling_rename = {col: 'last5_' + col for col in team_stat_cols}

rolling_stats = rolling_stats.rename(columns=rolling_rename)

df = pd.concat([df, rolling_stats], axis=1)

print(df.columns.tolist())

home_team_stats = df[df['player_team'] == df['match_home_team']]
away_team_stats = df[df['player_team'] == df['match_away_team']]

last5_cols = [col for col in df.columns if col.startswith('last5_')]

home_form = home_team_stats[['match_id'] + last5_cols].copy()
away_form = away_team_stats[['match_id'] + last5_cols].copy()

home_rename = {col: 'home_' + col for col in last5_cols}
away_rename = {col: 'away_' + col for col in last5_cols}

home_form = home_form.rename(columns=home_rename)
away_form = away_form.rename(columns=away_rename)

form_stats = pd.merge(home_form, away_form, on=['match_id'])

print(form_stats.shape)

match_stats = pd.read_csv("data/cleaned/match_stats.csv")
model_data = pd.merge(form_stats, match_stats[['match_id', 'match_date', 'match_round', 'venue_name',
                                                'match_home_team', 'match_away_team', 'home_margin']], 
                       on='match_id')
model_data.to_csv('data/cleaned/model_data.csv', index=False)
print(model_data.shape)

