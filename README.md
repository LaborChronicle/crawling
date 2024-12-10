# Labor Chronicle Crawler

## Overview

The Labor Chronicle Crawler is a component of the Labor Chronicle application, designed to gather labor-related news articles from news platforms and labor organizations. This crawler is specifically tuned to identify and retrieve news content that pertains to labor issues.

## Purpose

This crawler is developed to support public knowledge related to labor rights and developments. It helps consolidate news from various sources into a single, accessible platform, making it easier for users to stay informed about significant labor-related issues.

## Operational Details

- **Target Content**: The crawler is programmed to search for and retrieve articles that explicitly relate to labor topics. It uses predefined keywords and categories (such as "labor rights," "unions," "wages," "employment law") to filter content during the crawling process.
- **Frequency**: To minimize server load and respect the website's bandwidth, the crawler operates once daily during off-peak hours.
- **User-Agent String**: The crawler identifies itself with: `LaborChronicleCrawler/1.0 (+https://github.com/LaborChronicle/crawling)`

## Compliance with `robots.txt`

- **Adherence to Directives**: This crawler strictly adheres to the directives outlined in the `robots.txt` files of all target websites. It is configured to respect all `Disallow` and `Allow` rules to ensure compliance with each site's policy on automated access.
- **Respect for Site Architecture**: The crawler is designed to navigate and parse websites without causing undue strain or impact on their operational performance.

## Ethical Considerations

- **Data Use**: All data retrieved by this crawler is used for the sole purpose of aggregating news content related to labor issues. The data is used to provide direct links to the original articles on the native news platforms, ensuring full credit remains with the original publishers and authors.
- **Transparency**: We commit to transparency in our operations, providing clear contact information for any inquiries or concerns from web administrators or the public.

## Contact Information

For any inquiries, feedback, or concerns about the Labor Chronicle Crawler, please contact:

- **Email**: litaliencaleb@gmail.com
- **GitHub Repository**: [https://github.com/LaborChronicle/crawling](https://github.com/LaborChronicle/crawling)
