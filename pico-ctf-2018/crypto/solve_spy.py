from pwn import *

message_prefix = "Agent,\nGreetings. My situation report is as follows:\n"
message_suffix_before_flag = "\nMy agent identifying code is: "

AES_BLOCK = 16

def send_msg_and_get_response(msg):
  p = remote("2018shell2.picoctf.com", 34490)
  p.recvuntil("Please enter your situation report:")
 
  p.send(msg + "\n")
  resp = p.recvuntil("\n")
  p.close()

  return resp[1:]

def get_block_encryption(block):
  padding = "A" * (AES_BLOCK - (len(message_prefix) % AES_BLOCK))
  assert((len(message_prefix) + len(padding)) % 16 == 0)
  
  resp = send_msg_and_get_response(padding + block)
  resp_corresponding_to_block = resp[len(message_prefix + padding)*2:(len(message_prefix + padding) + AES_BLOCK)*2]

  print repr(resp)
  
  return resp_corresponding_to_block

def decrypt_next_byte_of_flag(known_prefix):
  if len(known_prefix) >= 16:
    actual_prefix = known_prefix[-15:]
    overlap = 0
  else:
    actual_prefix = message_suffix_before_flag[-(15 - len(known_prefix)):] + known_prefix
    overlap = 15 - len(known_prefix)

  length_without_padding = len(message_prefix) + len(message_suffix_before_flag) + len(known_prefix) 
  padding_length = (AES_BLOCK - 1 - (length_without_padding % AES_BLOCK))
  if padding_length < 0: padding_length += AES_BLOCK
  
  start_of_target_block = length_without_padding + padding_length - 15
  assert(start_of_target_block % 16 == 0)

  resp = send_msg_and_get_response("A" * padding_length)
  
  expected_block = resp[start_of_target_block*2:(start_of_target_block+AES_BLOCK) * 2]

  print expected_block

  for b in xrange(256):
    if b == 10: continue
    guess = get_block_encryption(actual_prefix + chr(b))
    print b, guess
    if b == guess: return chr(b)
  return None

decrypt_next_byte_of_flag("")

