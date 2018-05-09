library(shiny)
library(tidyverse)
library(data.table)

# df <- read.csv("names-all-years.csv")

# use data.table fread for increased speed
df <- fread("names-all-years.csv") %>% as.data.frame()
df <- select( df, -(V1))
head(df)
sortedUniqueNames <- unique(df$Name) %>% sort()

# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("Baby Name Analyzer"),
   tabsetPanel(type = "tabs",
               tabPanel("Popular Names", fluid = TRUE,
                 sidebarLayout(
                   sidebarPanel(
                    
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
                     plotOutput("nameTimeSeries"),
                     textOutput("test")
                   )
                 )
               )
   
   )
)
   # Sidebar with a slider input for number of bins 
   


# Define server logic required to draw a histogram
server <- function(input, output) {
   output$test <- renderText(input$selected_gender)
   
   # output$popular_plot <-renderText(filter(df, Year >= input$year_range[1] & Year <= input$year_range[2]))
   output$popular_plot <-renderPlot({
     filteredDF <- filter(df, Year >= input$year_range[1] & Year <= input$year_range[2]) %>% group_by(Name) %>% summarise(total = sum(n)) %>% arrange(desc(total),Name)
     
     ggplot(data=filteredDF[1:10,], aes(Name, total)) +
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

