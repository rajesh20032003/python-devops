import logging , requests

logger = logging.getLogger(__name__)

def check_urls(urls: list[str], timeout: int = 5) -> dict[str,str]:
  """
  Docstring for check_urls
  
  :param urls: Description
  :type urls: list[str]
  :param timeout: Description
  :type timeout: int
  :return: Description
  :rtype: dict[str, str]
  """
  logger.info(f"starting check for {len(urls)} with a timeout of {timeout}")
  results = {}
  
  for url in urls:
    status = "UNKNOWN"
    try:
      logger.debug(f"checking url: {url}")
      response = requests.get(url, timeout=timeout)
      if response.ok:
        status = f"{response.status_code} ok"
      else:
        status = f"{response.status_code} {response.reason}"
    except requests.exceptions.Timeout:
      status = 'TIMEOUT'
      logger.warning(f"request to {url} timed out")
    except requests.exceptions.ConnectionError:
      status = 'CONNECTIONERROR'
      logger.warning(f"request to {url} connection error ")
    except requests.exceptions.RequestException as e:
      status = f"REQUEST ERROR: {type(e).__name__}"
      logger.warning(f"An unexcepted request error occured for {url}:{e}",exc_info=True)
    results[url] = status
    logger.debug(f"checked: {url:<40} -> {status}") 
  logger.info("url check finished .")  
  return results
    
