options(repos = c(CRAN = "https://cran.rstudio.com/"))
# Pull AFL match data
install.packages("fitzRoy")
install.packages("dplyr")
install.packages("readr")

library(fitzRoy)
library(dplyr)
library(readr)

# Pull Fryzigg data from 2019 to 2026
player_stats <- fetch_player_stats_fryzigg(season = 2019:2026)

write_csv(player_stats, "data/raw/data_fryzigg.csv")
