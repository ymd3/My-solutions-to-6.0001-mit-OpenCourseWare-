# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
from datetime import tzinfo
from datetime import timezone
from datetime import timedelta
import pytz
from pytz import  timezone

#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        '''guid : A globaally unique identifier for this news story
        title : The new's story's headline
        description : A paragraph or so summarizing the news story
        link : a link to a website with the entire news story
        pubDate : Date the news was published
        category : News category, such as "Top Stories" '''
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        'returns guid'
        return self.guid

    def get_title(self):
        'returns title'
        return self.title

    def get_description(self):
        'returns description'
        return self.description

    def get_link(self):
        'returns link'
        return self.link

    def get_pubdate(self):
        'returns pubdate'
        return self.pubdate

    def __str__(self):
        print(self.get_guid(),self.get_pubdate(),self.get_description(),self.get_title(),self.get_link())
#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, string_phrase):
        self.string_phrase = string_phrase.lower()

    def get_string_phrase(self):
        return self.string_phrase

    def is_phrase_in(self, text):
        '''checks if the string phrase is in the text of this method. The words in the string phrase
        must only be seperated by spaces and punctuations. They also must be in the correct sequence.
        string_phrase is not case sensitive and all are in lower aphabets'''
        import string
        text = list(text)
        for char in text:
            if char in string.punctuation:
                a = text.index(char)
                text.remove(char)
                text.insert(a, ' ')

        removed = False
        while not removed:
            x = 0
            removed = True
            while x + 1 < len(text):
                if text[x] == ' ' and text[x + 1] == ' ':
                    text.pop(x)
                    removed = False
                x += 1

        text = ''.join(text)

        if self.get_string_phrase() in text.lower():
            phrase = self.get_string_phrase()
            phrase = phrase.split(' ')
            text = text.lower()
            text = text.split(' ')
            x = 0
            for phrases in phrase:
                if phrases in text:
                    x += 1
            if x == len(phrase):
                return True
            else:
                return False
        else:
            return False

# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, string_phrase):
        self.string_phrase = string_phrase.lower()

    def get_string_phrase(self):
        return self.string_phrase

    def evaluate(self, story):
        '''evaluates if the story should be alerted based on the title o fthe Newstory object.
        returns true should an alert be generated and falss otherwise '''
        if self.is_phrase_in(story.get_title().lower()) == True:
            return True
        else:
            return False

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, string_phrase):
        '''takes in the string_phrase as an argument'''
        self.string_phrase = string_phrase.lower()

    def get_string_phrase(self):
        return self.string_phrase

    def evaluate(self, story):
        '''evaluates the story should be alerted based on the description of the NewsStory object.
        Returns True should an alert be generated and false otherwise '''
        if self.is_phrase_in(story.get_description().lower()) == True:
            return True
        else:
            return False
# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
class Timetrigger(Trigger):
    def __init__(self, time):
        '''changes the time string into a datetime object that is aware.'''
        eastern = timezone('EST')
        date = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        date = eastern.localize(date)
        self.time = date

    def get_time(self):
        '''returns the time string into a date time object'''
        return self.time

# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(Timetrigger):
    def evaluate(self, story):
        datepub = story.get_pubdate()
        if datepub.tzinfo == None and datepub.utcoffset() == None:
            eastern = timezone("EST")
            datepub = eastern.localize(datepub)

        if datepub <= self.get_time():
            return True
        else:
            return False


class AfterTrigger(Timetrigger):
    def evaluate(self, story):
        datepub = story.get_pubdate()
        if datepub.tzinfo == None and datepub.utcoffset() == None:
            eastern = timezone("EST")
            datepub = eastern.localize(datepub)
        if datepub >= self.get_time():
            return True
        else:
            return False
# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    '''takes in another trigger as an argument and inverts if the trigger fires or not '''
    def __init__(self, trigger):
        self.trigger = trigger

    def get_trigger(self):
        return self.trigger

    def evaluate(self, story):
        if self.get_trigger().evaluate(story) == True:
            return False
        else:
            return True

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trig1 , trig2):
        self.trig1 = trig1
        self.trig2 = trig2

    def get_trig1(self):
        return self.trig1

    def get_trig2(self):
        return self.trig2

    def evaluate(self, story):
        if self.get_trig1().evaluate(story) == True and self.get_trig2().evaluate(story) == True:
            return True
        else:
            return False


# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trig1, trig2):
        self.trig1 = trig1
        self.trig2 = trig2

    def get_trig1(self):
        return self.trig1

    def get_trig2(self):
        return self.trig2

    def evaluate(self,story):
        if self.get_trig2().evaluate(story) == True or self.get_trig1().evaluate(story) == True:
            return True

        else:
            return False


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    relevant = []
    for story in stories:
        x = 0
        for triggers in triggerlist:
            if triggers.evaluate(story) == True:
                x += 1

        if x >= 1:
            relevant.append(story)

    return relevant



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    define = []
    for text in lines:
        text = text.split(',')
        if 'TITILE' in text:
            argument = text[2]
            trigger = TitleTrigger(argument)
            define.append(trigger)

        elif 'DESCRIPTION' in text:
            argument = text[2]
            trigger = DescriptionTrigger(argument)
            define.append(trigger)

        elif 'AFTER' in text:
            argument = text[2]
            trigger = AfterTrigger(argument)
            define.append(trigger)

        elif 'BEFORE' in text:
            argument = text[2]
            trigger = BeforeTrigger(argument)
            define.append(trigger)

        elif 'AND' in text:
            args_for_and = []
            for arg in text[2:]:
                a = list(arg)
                args_for_and.append(a[1])

            trig1 = define[len(args_for_and[0]) - 1]
            trig2 = define[len(args_for_and[1]) - 1]
            new_trig = AndTrigger(trig1,trig2)
            define.append(new_trig)


        elif 'Or' in text:
            args_for_and = []
            for arg in text[2:3]:
                args_for_and = []
                for arg in text[2:]:
                    a = list(arg)
                    args_for_and.append(a[1])

            trig1 = define[len(args_for_and[0]) - 1]
            trig2 = define[len(args_for_and[1]) - 1]
            new_trig = OrTrigger(trig1, trig2)
            define.append(new_trig)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

     # for now, print it so you see what it contains!
    return define


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("Conflict")
        t2 = DescriptionTrigger("Israel")
        t3 = DescriptionTrigger("Palestine")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            #stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    x = read_trigger_config('triggers.txt')
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
