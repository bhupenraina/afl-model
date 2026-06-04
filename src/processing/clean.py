import pandas as pd

df = pd.read_csv("data/raw/data_fryzigg.csv", low_memory = False)

team_stat_cols = ['kicks', 'marks', 'handballs', 'disposals', 'effective_disposals','hitouts', 'tackles', 'rebounds', 'inside_fifties', 'clearances', 'clangers', 'free_kicks_for', 'free_kicks_against','contested_possessions', 'uncontested_possessions', 'contested_marks', 'marks_inside_fifty', 'one_percenters', 'bounces', 'goal_assists','afl_fantasy_score', 'supercoach_score', 'centre_clearances', 'stoppage_clearances', 'score_involvements', 'metres_gained', 'turnovers', 'intercepts', 'tackles_inside_fifty', 'contest_def_losses', 'contest_def_one_on_ones', 'contest_off_one_on_ones', 'contest_off_wins', 'def_half_pressure_acts', 'effective_kicks', 'f50_ground_ball_gets', 'ground_ball_gets', 'hitouts_to_advantage','intercept_marks', 'marks_on_lead', 'pressure_acts', 'rating_points', 'ruck_contests', 'score_launches', 'shots_at_goal', 'spoils']

team_stats = df.groupby(['match_id', 'match_date', 'match_round', 'venue_name',
                          'match_home_team', 'match_away_team',
                          'match_home_team_score', 'match_away_team_score',
                          'player_team'])[team_stat_cols].sum().reset_index()

print(team_stats.columns.tolist())

print(team_stats.shape)

home_team_stats = team_stats[team_stats['player_team'] == team_stats['match_home_team']]
away_team_stats = team_stats[team_stats['player_team'] == team_stats['match_away_team']]

print(home_team_stats.shape)
print(away_team_stats.shape)

print(home_team_stats.columns.tolist())

home_rename = {col: 'home_' + col for col in team_stat_cols}
away_rename = {col: 'away_' + col for col in team_stat_cols}

home_team_stats = home_team_stats.rename(columns=home_rename)
away_team_stats = away_team_stats.rename(columns=away_rename)

home_team_stats = home_team_stats.drop(columns=['player_team'])
away_team_stats = away_team_stats.drop(columns=['player_team'])

match_stats = pd.merge(home_team_stats, away_team_stats, 
                        on=['match_id', 'match_date', 'match_round', 'venue_name',
                            'match_home_team', 'match_away_team',
                            'match_home_team_score', 'match_away_team_score'])

print(match_stats.shape)

match_stats['home_margin'] = match_stats['match_home_team_score'] - match_stats['match_away_team_score']

print(match_stats.shape)

match_stats.to_csv('data/cleaned/match_stats.csv', index=False)
