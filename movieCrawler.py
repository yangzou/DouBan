# Step 1: Import necessary packages to your application
import requests
import json
import time
import sys

# Create a method that queries all movies from a given year
class DouBanMovieCrawler:
    def crawlMovies(self, year, collect_count):
        totalNumber = -1
        start = 0
        interestingMovies = []
        curr = None

        while totalNumber < 0 or start < totalNumber:
            try:
                url = "https://api.douban.com/v2/movie/search?q=%s&start=%s" %(year, start)
                r = requests.get(url).json()

                if('msg' in r and r.get('msg').startswith('rate_limit_exceeded')):
                    print ('API limit reached. Will sleep 30 minutes')
                    print ('Response: %s' % json.dumps(r))
                    time.sleep(30*60)
                    continue

                if (totalNumber == -1):
                    # We only need to set totalNumber once
                    totalNumber = int(r.get('total'))

                # Increment the start count so that next search will start from where the previous search ends
                start += int(r.get('count'))
                print ('Got %s movies, total %s' %(start, totalNumber))

                movies = r.get('subjects')
                for movie in movies:
                    curr = movie
                    if int(movie.get('year')) == year and int(movie.get('collect_count')) >= collect_count:
                        interestingMovies.append(movie)

            except:
                print ('Exception: %s' % str(sys.exc_info()))
                print (json.dumps(curr, sort_keys=True, indent=4))

        print ('Found %s interesting movies' %len(interestingMovies))
        print ('Output file: output.json')

        with open('output.json', 'w') as outfile:
            json.dump(interestingMovies, outfile, indent=4, sort_keys=True);

        # End of crawlMovies
# End of DouBanMovieCrawler class

crawler = DouBanMovieCrawler()
crawler.crawlMovies(2015, 1000)
