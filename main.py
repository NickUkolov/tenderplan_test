import itertools

from celery import group

from celery_app import fetch_task, parse_xml_task


def process_tenders():
    base_url = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber="
    url_list = (f"{base_url}{page_num}" for page_num in range(1, 3))
    tender_tasks = group([fetch_task.s(el) for el in url_list])

    tender_print_urls = tender_tasks().get()

    result_tasks = group(
        [
            parse_xml_task.s(el)
            for el in itertools.chain.from_iterable(tender_print_urls)
        ]
    )
    result = result_tasks().get()

    for link, publish_date in result:
        print(f"Link: {link}, Publish Date: {publish_date}")


if __name__ == "__main__":
    process_tenders()
