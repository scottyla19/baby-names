library(shiny)
library(tidyverse)
library(data.table)

# df <- read.csv("names-all-years.csv")

# use data.table fread for increased speed
df <- fread("names-all-years.csv") %>% as.data.frame()
df <- select( df, -(V1))

sortedUniqueNames <- unique(df$Name) %>% sort()

# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("Baby Name Analyzer"),
   tabsetPanel(type = "tabs",
               tabPanel("Popular Names", fluid = TRUE,
                 sidebarLayout(
                   sidebarPanel(
                     radioButtons("selected_gender", label = "Select a gender:",
                                  choices = list("Female" = "F", "Male" = "M", "Either" = "E"), 
                                  selected = "F"),
                     sliderInput("year_range",
                                 "Range of Years",
                                 min = 1880,
                                 max = 2016,
                                 step = 1,
                                 value = c(2000, 2016))
                     ),
                  
                   
                   # Show a plot of the generated distribution
                   mainPanel(
                     plotOutput("popular_plot")
                     
                   )
                 )
               ),
               tabPanel("Names Over Time", fluid = TRUE,
                 sidebarLayout(
                   sidebarPanel(
                     radioButtons("selected_gender", label = "Select a gender:",
                                  choices = list("Female" = "F", "Male" = "M", "Either" = "E"), 
                                  selected = "F"),
                     selectInput("selected_name",
                                 "Select a Name:",
                                 sortedUniqueNames
                     )
                   ),
                   
                   mainPanel(
                     plotOutput("nameTimeSeries")
                   )
                 )
               )
   
   )
)
   # Sidebar with a slider input for number of bins 
   


# Define server logic required to draw a histogram
server <- function(input, output) {

   output$popular_plot <-renderPlot({
     filteredDF <- filter(df, Year >= 2000 & Year <= 2016 & Gender == "M") %>% 
       group_by(Name, Gender) %>% 
       summarise(total = sum(n)) %>% 
       arrange(desc(total)) %>%
       top_n((10))
     
     girlsDF <- filter(df, Year >= 2000 & Year <= 2016 & Gender == "F") %>% 
       group_by(Name, Gender) %>% 
       summarise(total = sum(n)) %>% 
       arrange(desc(total)) %>%
       top_n(10)
     
     if (input$selected_gender == "E") {
       filteredDF <- rbind(girlsDF, filteredDF)
     } else if (input$selected_gender == "F"){
       filteredDF <- girlsDF
     }
     

     ggplot(data=filteredDF, aes(Name, total, color = Gender)) +
       geom_col()
   })

   
   output$nameTimeSeries <- renderPlot({
     filteredDF <- filter(df,Name == input$selected_name)
    
     if (input$selected_gender != "E") {
       filteredDF <- filter(filteredDF,Gender == input$selected_gender)
     }
     ggplot(data=filteredDF, aes(x=Year, y=n, group = Gender, color=Gender)) +
       geom_line()+
       geom_point()
   })
}

# Run the application 
shinyApp(ui = ui, server = server)

