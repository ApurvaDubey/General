
# About: this code performs geo-spatial clustering
# this is like KMC, but on geo-spatial data

library(geosphere)
library(cluster)
library(fossil)
library(sqldf)

# read inputs
input <- airports <- read.csv("http://sourceforge.net/p/openflights/code/HEAD/tree/openflights/data/airports.dat?format=raw", header = FALSE)
colnames(airports) <- c("AIRPORT_ID","NAME","CITY","CNTRY","IATA","ICAO","LAT","LONG","ALT","TZ","DST","TZDBT")

# subset to data corresponding to India
data <- input[which(input$CNTRY=='India'),]

# change CITY from factor to string - this will be useful later
data$CITY = as.character(data$CITY)

# create clusters
clusteramounts <- 6
distance.matrix <- (distm(data[,c("LONG","LAT")]))
clustersx <- as.hclust(agnes(distance.matrix, diss = T))
data$cluster <- cutree(clustersx, k=clusteramounts)

# find countt of elements in each cluster
# if there is a cluster with less than 3 elements then flat it out
x <- sqldf("select cluster, count(1) as cluster_cnt from data group by cluster ",row.names=FALSE)
x$flag <- ifelse(x$cluster_cnt < 3, 0, 1)

################

# show clusters on a map
library(ggmap)
library(mapproj)
map <- get_map(location = 'India', zoom = 5)
ggmap(map)

mapPoints <- ggmap(map) + 
  geom_point(aes(x = LONG, y = LAT, size = 1, color=as.factor(cluster), shape=as.factor(cluster)), data = data)
plot(mapPoints)

#############

# calcuate area of each cluster, and corresponding radius
for (i in 1:clusteramounts) {
  
  if(x[i,]$flag==1) {
    A = earth.poly(points.to.group[which(points.to.group$group==i),c("LONG","LAT")]) 
    x[i,]$Area = A$area
    x[i,]$Radius = (A$area/pi)
  }
  else {
    print ("Not possible") 
  }
  
}

###################

# write output
write.csv(data, file = "clusters.txt",row.names=FALSE)
write.csv(x, file = "cluster_summary.txt",row.names=FALSE)


###################

# calculate pair-wise distance
n = nrow(data)*nrow(data)
df <- data.frame(CITY1 = character(n), CITY2 = character(n), dist = numeric(n), stringsAsFactors = FALSE)
idx=0

for (i in 1:nrow(data)) {
    for (j in 1:nrow(data)) {
      idx = idx + 1
      p1=c(as.numeric(data[i,]$LONG),as.numeric(data[i,]$LAT))
      p2=c(as.numeric(data[j,]$LONG),as.numeric(data[j,]$LAT))
      d = distHaversine(p1,p2,r=6378137)
      #print(c(p1,p2,d))
      #print (c(data[i,]$CITY,data[j,]$CITY,d))
      df$CITY1[idx]=data[i,]$CITY
      df$CITY2[idx]=data[j,]$CITY
      df$dist[idx]=d
      
      #print (c(data[i,]$CITY, data[i,]$LONG,data[i,]$LAT,data[j,]$CITY,data[j,]$LONG,data[j,]$LAT,d))
    }
}

write.csv(df, file = "pairwise_dist.txt",row.names=FALSE)

