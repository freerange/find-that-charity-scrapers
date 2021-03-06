# -*- coding: utf-8 -*-
import datetime
import io
import csv
import zipfile

import scrapy

from .base_scraper import BaseScraper
from ..items import Organisation, Source

class OSCRSpider(BaseScraper):
    name = 'oscr'
    allowed_domains = ['oscr.org.uk', 'githubusercontent.com']
    start_urls = [
        "https://www.oscr.org.uk/umbraco/Surface/FormsSurface/CharityRegDownload",
        "https://www.oscr.org.uk/umbraco/Surface/FormsSurface/CharityFormerRegDownload",
    ]
    org_id_prefix = "GB-SC"
    id_field = "Charity Number"
    date_fields = ["Registered Date", "Year End", "Ceased Date"]
    date_format = {
        "Registered Date": "%d/%m/%Y %H:%M",
        "Ceased Date": "%d/%m/%Y %H:%M",
        "Year End": "%d/%m/%Y"
    }
    source = {
        "title": "Office of Scottish Charity Regulator Charity Register Download",
        "description": "",
        "identifier": "oscr",
        "license": "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/",
        "license_name": "Open Government Licence v2.0",
        "issued": "",
        "modified": "",
        "publisher": {
            "name": "Office of Scottish Charity Regulator",
            "website": "https://www.oscr.org.uk/",
        },
        "distribution": [
            {
                "downloadURL": "",
                "accessURL": "",
                "title": "Office of Scottish Charity Regulator Charity Register Download"
            }
        ],
    }

    def start_requests(self):
        return [
            scrapy.Request(self.start_urls[0], callback=self.process_zip),
            scrapy.Request(self.start_urls[1], callback=self.process_zip),
        ]


    def process_zip(self, response):
        csvs = []
        self.logger.info("File size: {}".format(len(response.body)))
        with zipfile.ZipFile(io.BytesIO(response.body)) as z:
            for f in z.infolist():
                self.logger.info("Opening: {}".format(f.filename))
                with z.open(f) as csvfile:
                    csvs.append(response.replace(
                        body=csvfile.read()))
        return self.parse_csv(csvs[0])

    def parse_row(self, record):

        record = self.clean_fields(record)

        address, _ = self.split_address(record.get("Principal Office/Trustees Address", ""), get_postcode=False)

        org_types = [
            "Registered Charity",
            "Registered Charity (Scotland)",
        ]
        if record.get("Regulatory Type") != "Standard":
            org_types.append(record.get("Regulatory Type"))
        if record.get("Designated religious body") == "Yes":
            org_types.append("Designated religious body")
        
        if record.get("Constitutional Form") == "SCIO (Scottish Charitable Incorporated Organisation)":
            org_types.append("Scottish Charitable Incorporated Organisation")
        elif record.get("Constitutional Form") == "CIO (Charitable Incorporated Organisation, E&W)":
            org_types.append("Charitable Incorporated Organisation")
        elif record.get("Constitutional Form") == "Company (the charity is registered with Companies House)":
            org_types.append("Registered Company")
            org_types.append("Incorporated Charity")
        elif record.get("Constitutional Form") == "Trust (founding document is a deed of trust) (other than educational endowment)":
            org_types.append("Trust")
        elif record.get("Constitutional Form") != "Other":
            org_types.append(record.get("Constitutional Form"))

        org_ids = [self.get_org_id(record)]

        return Organisation(**{
            "id": self.get_org_id(record),
            "name": record.get("Charity Name"),
            "charityNumber": record.get(self.id_field),
            "companyNumber": None,
            "streetAddress": address[0],
            "addressLocality": address[1],
            "addressRegion": address[2],
            "addressCountry": "Scotland",
            "postalCode": self.parse_postcode(record.get("Postcode")),
            "telephone": None,
            "alternateName": [record.get("Known As")] if record.get("Known As") else [],
            "email": None,
            "description": record.get("Objectives"),
            "organisationType": org_types,
            "organisationTypePrimary": "Registered Charity",
            "url": self.parse_url(record.get("Website")),
            "location": [],
            "latestIncome": int(record["Most recent year income"]) if record.get("Most recent year income") else None,
            "dateModified": datetime.datetime.now(),
            "dateRegistered": record.get("Registered Date"),
            "dateRemoved": record.get("Ceased Date"),
            "active": record.get("Charity Status") != "Removed",
            "parent": record.get("Parent Charity Name"), # @TODO: More sophisticated getting of parent charities here
            "orgIDs": org_ids,
            "source": self.source["identifier"],
        })
