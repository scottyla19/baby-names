library(tidyverse)


df <- read.csv("data/yob1880.txt", header = FALSE) %>%
    rename(Name = V1, Gender = V2, n =  V3) %>%
    mutate(Year = 1880)

for(i in 1881:2016) {
  currentFile <- sprintf("data/yob%d.txt", i)
  df2 <- read.csv(currentFile, header = FALSE) %>%
    rename(Name = V1, Gender = V2, n =  V3) %>%
    mutate(Year = i)
  df <- rbind(df, df2)
  
}
df <- arrange(df, Name, Year)
write.csv(df, file = "data/names-all-years.csv")

