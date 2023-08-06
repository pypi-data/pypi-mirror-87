"""
Create, list or view the status of URLs registered in Autoseeder.

Usage:
  autoseeder-cli list [--limit=<limit>] [--desc]
  autoseeder-cli get_csv <output_file>
  autoseeder-cli submit <url> [--seed-region=<seed-region>]
  autoseeder-cli find_urls <url_search_term>
  autoseeder-cli view <submission>
  autoseeder-cli save_screenshot <uuid> <output_file> [--show-url]
  autoseeder-cli save_screenshots <uuid> <output_path> [--show-url]
  autoseeder-cli save_screenshots_all <uuid> <output_path> [--show-url]
  autoseeder-cli get_token


Options:
  list               List all URLs submitted into Autoseeder by submission time
    --limit=<limit>    Add a limit for number of records to show, 0 for no limit [default: 30]
    --desc             Order by submission time in descending order rather than ascending

  get_csv            Download a CSV of all URLs submitted into Autoseeder and the results.
    output_file         File path to save to

  submit             Submit a new URL to Autoseeder for seeding
    url                URL to be seeded
    --seed-region=<seed-region>
                       Optionally limit seeding source to particular country code
                       (e.g. "AU", "NZ", "AU,NZ" for multiple regions)

  find_urls          Returns UUID of URLs matching search_term
    url_search_term    Part or all of a URL to match on

  view               View detailed data for a single URL
    submission         UUID or URL of Autoseeder submission to view

  save_screenshot    Save single screenshot file based on screenshot UUID
    uuid               UUID of screenshot to save (n.b. different to URL UUIDs)
    output_file        File path to save to
    [--show-url]       If specified - render the URL for a screenshot in  a chromium-like address bar

  save_screenshots   Save onload screenshots for a URL into a directory.
                     Form fields will be default / blank.
    uuid               UUID of URL
    output_path        Directory path to save screenshots into; will be created
                       if necessary
    [--show-url]       If specified - render the URL for a screenshot in  a chromium-like address bar

  save_screenshots_all
                     Save onload and onsubmit screenshot files for a URL.
    uuid               UUID of URL
    output_path        Directory path to save screenshots into; will be created
                       if necessary
    [--show-url]       If specified - render the URL for a screenshot in  a chromium-like address bar

  get_token          Get a token if you have a username and password

  show_config        Print the resultant configuration file (to STDOUT) that autoseeder-cli would run one of the above commands with.

  -h help          Show this screen.
  --version        Show version.

Required environment variables:
  AUTOSEEDER_BASE_URL  The URL that the Autoseeder service resides at [e.g.: https://myinstance.autoseeder.cosive.com/autoseeder/]
  AUTOSEEDER_TOKEN     Token to connect with

Optional environment variables:
  AUTOSEEDER_LOG_LEVEL Select logging detail level from [ERROR, WARNING, INFO, DEBUG]
  AUTOSEEDER_TOKEN is required for all sub-command except get_token
  AUTOSEEDER_USER and AUTOSEEDER_PASS are required for the get_token sub-command
"""

__version__ = "2.7.0"
__description__ = "The autoseeder-cli tools allow you to interact easily with the Autoseeder API to submit new URLs " \
                  "and check the status of existing URLs."
__copyright__ = "Copyright 2019 Cosive Pty Ltd"
__license__ = "Apache 2.0"
import docopt
import sys
import os.path

from .util import process_env_args, logger, ENV_VAR_DEFS
from .as_cli_actions import *


def do_submit(url, seed_regions_str, **kwargs):
    action = AutoseederSubmitter(**kwargs)
    resp = action.submit_url(url, seed_regions_str=seed_regions_str)

    logger.warning("URL successfully submitted, UUID assigned")
    print(resp.get('uuid'))


def do_list(**kwargs):
    print(AutoseederLister(**kwargs).format_report())


def do_find_urls(url_search_term, **kwargs):
    searcher = AutoseederSearcher(**kwargs)
    for uuid in searcher.find_urls(url_search_term):
        print(uuid)


def do_view(val, **kwargs):
    import json
    from uuid import UUID
    action = AutoseederURLViewer(**kwargs)
    searcher = AutoseederSearcher(**kwargs)
    try:
        try:
            _ = UUID(val)
            is_uuid = True
        except:
            is_uuid = False
        if not is_uuid:
            out_data = []
            for uuid in searcher.find_urls(val):
                out_data.append(json.loads(action.get_url_data(uuid)))
            print(json.dumps(out_data, indent=2))
        else:
            print(action.get_url_data(val))
    except ValueError as err:
        print(
            f"error: Unable to find a URL matching {val}.\nNote that wild card or multiple searches will not work.\n",
            err)


def do_get_token(**kwargs):
    action = AutoseederTokenGetter(**kwargs)
    print(action.get_token())


def do_save_screenshot(uuid, output_file, render_addressbar, **kwargs):
    action = AutoseederScreenshotDownloader(**kwargs)
    file_content = action.get_screenshot(uuid, render_addressbar)
    try:

        with open(output_file, 'wb') as out:
            out.write(file_content)

        logger.info('Wrote {} bytes to {}'.format(len(file_content), output_file))
        sys.exit(0)
    except Exception as err:
        logger.exception('Failed to write to output file')
        print(f"error: '{file_content}': failed to write to output", err)


def do_save_screenshots(uuid, output_path, render_addressbars=False, **kwargs):
    from json import loads
    url_info_action = AutoseederURLViewer(**kwargs)
    url_info_json = url_info_action.get_url_data(uuid)
    url_info = loads(url_info_json)

    logger.debug('Received response: ')
    logger.debug(url_info_json)

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        logger.info('Created directory {}'.format(output_path))

    if 'detail' not in url_info:
        logger.warning('No details available for the specified URL')
        sys.exit(1)

    if len(url_info['detail']) == 0:
        logger.warning('The specified submission has not been processed yet')
        sys.exit(1)

    kit = None
    if len(url_info['detail']) == 1:
        kit = url_info['detail'][0]
    else:
        # Sweeping assumption here - the most recent unique fingerprint for the submission ID
        # is considered the appropriate source for screenshots.
        kit = url_info['detail'][-1]

    images_saved = 0

    for run_index, run in enumerate(kit['seeding_results']):
        if 'breakdown' not in run:
            logger.debug('skipping run {} - no breakdown defined'.format(run_index))
            continue

        for page_index, page_in_run in enumerate(run['breakdown']):
            if 'screenshot_onload' not in page_in_run:
                logger.debug('skipping page {} - no screenshot defined'.format(page_index))
                continue

            output_filename = os.path.join(output_path, 'run{}-page{}.png'.format(run_index, page_index))
            download_action = AutoseederScreenshotDownloader(**kwargs)
            img = download_action.get_screenshot(page_in_run['screenshot_onload']['uuid'], render_addressbars)
            with open(output_filename, 'wb') as out:
                out.write(img)
                images_saved += 1
                logger.info('Wrote {} bytes to {}'.format(len(img), output_filename))

    if images_saved <= 0:
        logger.warning('No screenshots attached to the specified URL (nothing saved to disk)')
        sys.exit(1)

    sys.exit(0)


def do_save_all_screenshots(uuid, output_path, render_addressbars=False, **kwargs):
    from json import loads
    url_info_action = AutoseederURLViewer(**kwargs)
    url_info_json = url_info_action.get_url_data(uuid)
    url_info = loads(url_info_json)

    logger.debug('Received response: ')
    logger.debug(url_info_json)

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        logger.info('Created directory {}'.format(output_path))

    if 'detail' not in url_info:
        logger.warning('No details available for the specified URL')
        sys.exit(1)

    images_saved = 0

    for kit_index, kit in enumerate(url_info['detail']):
        logger.debug('processing kit#{}'.format(kit_index))
        for run_index, run in enumerate(kit['seeding_results']):
            if 'breakdown' not in run:
                logger.debug('skipping kit {}, run {} - no breakdown defined'.format(kit_index, run_index))
                continue

            for page_index, page_in_run in enumerate(run['breakdown']):
                for event in ['onload', 'onsubmit']:
                    if 'screenshot_' + event not in page_in_run:
                        logger.debug('skipping page {} - no screenshot defined'.format(page_index))
                        continue

                    output_filename = os.path.join(output_path, 'kit{}-run{}-page{}-{}.png'.format(kit_index, run_index, page_index, event))
                    download_action = AutoseederScreenshotDownloader(**kwargs)
                    img = download_action.get_screenshot(page_in_run['screenshot_' + event]['uuid'], render_addressbars)
                    with open(output_filename, 'wb') as out:
                        out.write(img)
                        images_saved += 1
                        logger.info('Wrote {} bytes to {}'.format(len(img), output_filename))

    if images_saved <= 0:
        logger.warning('No screenshots attached to the specified URL (nothing saved to disk)')
        sys.exit(1)

    sys.exit(0)


def do_get_csv_data(output_file, **kwargs):
    get_csv_action = AutoseederCSVDownloader(**kwargs)
    csv_data = get_csv_action.get_csv_data()
    try:
        with open(output_file, 'wb') as out:
            out.write(csv_data.encode('utf-8'))

        sys.exit(0)
    except Exception as err:
        logger.exception('Failed to write to output file')
        print(f"error: failed to write to output", err)


def main(args):
    try:
        logger.debug(args)

        if args.get("show_config"):
            env_vars = process_env_args()
            for k, v in ENV_VAR_DEFS.items():
                print(f'\t{k} => {env_vars[k]}')

        if args.get("list"):
            env_vars = process_env_args()
            do_list(limit=args["--limit"], desc=args["--desc"], base_url=env_vars["base_url"], token=env_vars["token"])
        elif args.get("get_csv"):
            env_vars = process_env_args()
            do_get_csv_data(args["<output_file>"], base_url=env_vars["base_url"], token=env_vars["token"])
        elif args.get("submit"):
            env_vars = process_env_args()
            do_submit(args["<url>"], args["--seed-region"], base_url=env_vars["base_url"], token=env_vars["token"])
        elif args.get("find_urls"):
            env_vars = process_env_args()
            do_find_urls(args["<url_search_term>"], base_url=env_vars["base_url"], token=env_vars["token"])
        elif args.get("view"):
            env_vars = process_env_args()
            do_view(args["<submission>"], base_url=env_vars["base_url"], token=env_vars["token"])
        elif args.get("save_screenshot"):
            env_vars = process_env_args()
            do_save_screenshot(args["<uuid>"], args["<output_file>"], args["--show-url"], base_url=env_vars["base_url"],
                               token=env_vars["token"])
        elif args.get("save_screenshots"):
            env_vars = process_env_args()
            do_save_screenshots(args["<uuid>"], args["<output_path>"], args["--show-url"], base_url=env_vars["base_url"],
                                token=env_vars["token"])
        elif args.get("save_screenshots_all"):
            env_vars = process_env_args()
            do_save_all_screenshots(args["<uuid>"], args["<output_path>"], args["--show-url"],
                                    base_url=env_vars["base_url"], token=env_vars["token"])
        elif args.get("get_token"):
            env_vars = process_env_args(token_auth_vars=False)
            do_get_token(base_url=env_vars["base_url"], user=env_vars["user"], password=env_vars["pass"])

    except Exception as e:
        import traceback
        logger.debug(traceback.format_exc())
        sys.exit("Error: {}".format(e))


def entry_point():
    """
    Use entry_point() for script / setup.py purposes.
    main() receives the args dict so we can manipulate for testing purposes.
    """
    args = docopt.docopt(__doc__, version='Autoseeder Submission CLI v' + str(__version__))
    main(args)


if __name__ == '__main__':
    entry_point()
