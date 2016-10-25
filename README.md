oSoc17-website
==============

Website for open Summer of code 2017

-- It's a clone of an early version of the oSoc14 website. For more up to date features, steal from https://github.com/oSoc17/website

# Deployment

Make sure bower is installed

> npm install -g bower

Install other npm dependencies (only needed for Dev)

> npm install

Go to root folder of project in CLI

Run following command:

> bower update

This should install the jQuery, Modernizr and FontAwesome packages

> gulp

Compiles the SCSS files. (Only need to run this when you change the .scss files)

Everything should now be into place to upload the site.

## JSON-LD Event Information

Currently, the JSON LD only contains the mother Event of oSoc15, spanning the entire duration.
As soon as we have more information, we should add the subEvents for every day.

```json
{
          "@context" : "http://schema.org",
          "@type" : "Event",
          "name" : "Open Summer of code 2017",
          "startDate" : "2017-07-03T09:00",
          "endDate" : "2017-07-28T17:00",
          "organizer" : {
                "@id" : "https://opencorporates.com/id/companies/be/0845419930",
                "@type": "Organization",
                "name": "Open Knowledge Belgium",
                "url" : "http://www.openknowledge.be"
          },
          "location" : {
             "@type" : "Place",
             "name" : "TBA",
             "address" : "TBA"
          },
          "image" : "http://2017.summerofcode.be/images/socialmedia/logo.png"
      }
```

### subEvents

This part of the code can just be added after the  "image" : ".../logo.png" line, seperated by a comma.
It would also be nice to use URIs for the locations once they are defined.

```json
"subEvent" : [{
        "@type" : "Event",
        "name" : "Introduction",
        "startDate" : "2014-07-06T09:30",
        "endDate" : "2014-07-06T10:30",
        "organizer" : { "@id": "https://opencorporates.com/id/companies/be/0845419930"},
        "location" : { 
           "@type" : "Place",
           "name" : "TBA",
           "address" : "TBA"
        }
    }, 
    {
        "@type" : "Event",
        "name" : "Project assignment",
        "startDate" : "2014-07-06T11:00",
        "endDate" : "2014-07-06T12:00",
        "organizer" :{ "@id": "https://opencorporates.com/id/companies/be/0845419930"},
        "location" : { 
           "@type" : "Place",
           "name" : "TBA",
           "address" : "TBA"
        }
    }]
```
