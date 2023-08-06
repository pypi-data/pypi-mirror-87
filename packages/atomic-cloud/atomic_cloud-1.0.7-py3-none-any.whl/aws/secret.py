from aws.region import get_secret
import json
import time


def get_secret_value(name: str, key: str = None):
  """
  Gets a secret's value. By default, this gets the string value. If that string is a json object, you can supply a key to get the value from.

  :param name: The name of the secret you're looking for. If this is a secret in your account, the 'friendly' name is acceptable. If you want a secret from another account, you need to supply the entire ARN.
  :param key: If the secret is a StringSecret, you can supply a key. If you do, we return the value of that key in the StringSecret parsed as JSON.
  """
  try:
    response = get_secret().get_secret_value(SecretId = name)
  except:
    return None # secret doesn't exist

  if response.get('SecretString'):
    j = response.get('SecretString')
    if key:
      return json.loads(j).get(key)
    return j
  else:
    return response.get('SecretBinary')


def create_secret(name: str, description: str = "", binary: bytes = None, string: str = None, kvp: dict = None, tags: dict = None):
  """
  Creates a secret with either a binary or string/json value. You cannot supply both a binary and string value, but you must supploy one.

  :param name: The (friendly) name of the secret you're creating. Must be unique.
  :param description: The description of that secret (optional).
  :param binary: Binary data to store in the secret. 
  :param string: String value to store in the secret. If this is a valid json dict, you can access a key using our get_secret_value() function.
  :param tags: dict of key/value pairs to set as tags on the secret (optional).
  """
  if (binary is not None and (string or kvp)) or (string and kvp):
    raise Exception("You cannot provide multiple types of values for one secret.")

  if tags:
    formatted_tags_list = []
    for key in tags:
      formatted_tags_list.append({'Key': key, 'Value': tags[key]})
  else:
    formatted_tags_list = None
  
  if kvp:
    string = json.dumps(kvp)

  if formatted_tags_list:
    if binary:
      r = get_secret().create_secret(Name = name, Description = description, SecretBinary = binary, Tags = formatted_tags_list)
    else: # string
      r = get_secret().create_secret(Name = name, Description = description, SecretString = string, Tags = formatted_tags_list)
  else:
    if binary:
      r = get_secret().create_secret(Name = name, Description = description, SecretBinary = binary)
    else: # string
      r = get_secret().create_secret(Name = name, Description = description, SecretString = string)

  # add to r
  r['Description'] = description
  if binary:    
    r['SecretBinary'] = binary
  else:
    r['SecretString'] = string
  if tags:
    r['Tags'] = formatted_tags_list
  return r


def update_secret(name: str, binary = None, string: str = None, kvp: dict = None, overwriteJson: bool = False):
  """
  Updates a secret. If you supply a binary or string, that becomes the new value of the secret. If you supply a dict, that dict's values
  are added to the json-formatted string in the secret (or overwrites the string if it was not json).

  :param name: The name of the secret you're updating. If the secret is in your account, this can be the 'friendly' name or ARN. Otherwise, it must be the ARN.
  :param binary: Binary data to update the secret with. Overwrites the content of the secret.
  :param string: String to update the secret with. Overwrites the content of the secret.
  :param kvp: Dictionary of string/string pairs to update the secret with. These pairs get added to the existing json dictionary (if it exists).
  :param overwriteJson: If this is true, kvp will overwrite an existing dictionary rather than add its pairs to it (defaults to False).
  """

  if (binary is not None and (string or kvp)) or (string and kvp):
    raise Exception("You cannot provide multiple types of values for one secret.")

  existing = get_secret_value(name)
  try:
    existing_json = json.loads(existing)
    use_json = True
  except:
    use_json = False
  if use_json:
    if overwriteJson:
      secret_string = json.dumps(kvp)
      r = get_secret().update_secret(SecretId = name, SecretString = secret_string)
      r['SecretString'] = wait_for_secret(name, value=secret_string)
    else:
      for k in kvp:
        existing_json[k] = kvp[k]
      secret_string = json.dumps(existing_json)
      r = get_secret().update_secret(SecretId = name, SecretString = secret_string)
      r['SecretString'] = wait_for_secret(name, value=secret_string)
  elif type(existing) is str:
    r = get_secret().update_secret(SecretId = name, SecretString = string)
    r['SecretString'] = wait_for_secret(name, value=string)
  else: # binary
    r = get_secret().update_secret(SecretId = name, SecretBinary = binary)
    r['SecretBinary'] = wait_for_secret(name, value=binary)
  return r


def delete_secret(name: str, recovery_window: int = None, perma_delete: bool = False):
  """
  Deletes a secret. We do not recommend using the permanent deletion feature for otherwise inaccessible secrets!

  :param name: The name of the secret you're deleting. If the secret is in your account, this can be the 'friendly' name or ARN. Otherwise, it must be the ARN.
  :param recovery_window: The amount of days to wait before permanently deleting the secret. Minimum is 7, maximum is 30. Defaults to 7. Cannot be present if perma_delete is True.
  :param perma_delete: If True, we delete the secret permanently (without a 7-30 day recovery window). Cannot be True if recovery_window is supplied. Defaults to False.
  """
  if recovery_window and perma_delete:
    raise Exception("You cannot both specify a recovery window and force deletion without a recovery window")
  if not recovery_window or recovery_window < 7:
    recovery_window = 7
  if recovery_window > 30: recovery_window = 30
  try:
    if perma_delete:
      get_secret().delete_secret(SecretId = name, ForceDeleteWithoutRecovery = True)
      return True
    else:
      get_secret().delete_secret(SecretId = name, RecoveryWindowInDays = recovery_window)
  except:
    return False # the secret doesn't exist
  return recovery_window


def wait_for_secret(name: str, value = None, timeout: int = 60):
  """
  Wait for a secret to have the given value.
  This is useful for synchronization purposes, as updates to secrets are not always immediately reflected in subsequent requests.

  :param name: The name of the secret to wait on.
  :param value: The value to wait for. If None, will wait for secret to be deleted.
  :param timeout: The maximum time to wait, after which an Exception will be thrown. Default is 60 seconds.
  :return: The secret value, once it matches
  """
  for i in range(timeout):
    found = get_secret_value(name)
    if found == value:
      return found
    time.sleep(1)
  raise TimeoutError('Secret did not change to the expected value')