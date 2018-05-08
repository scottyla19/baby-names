library(shiny)
library(tidyverse)

df <- read.csv("names-all-years.csv")
df <- select( df, -(X))
sortedUniqueNames <- unique(df$Name) %>% sort()

# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("Baby Name Analyzer"),
   
   # Sidebar with a slider input for number of bins 
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
      
      # Show a plot of the generated distribution
      mainPanel(
         plotOutput("nameTimeSeries"),
         textOutput("test")
      )
   )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
   output$test <- renderText(input$selected_gender)
   
   
   output$nameTimeSeries <- renderPlot({
     filteredDF <- filter(df,Name == input$selected_name)
    
     if (input$selected_gender != "E") {
       filteredDF <- filter(filteredDF,Gender == input$selected_gender)
     }
     ggplot(data=filteredDF, aes(x=Year, y=Count, group = Gender, color=Gender)) +
       geom_line()+
       geom_point()
   })
}

# Run the application 
shinyApp(ui = ui, server = server)

