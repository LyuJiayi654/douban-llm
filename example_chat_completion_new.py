# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

from typing import List, Optional

import fire

from llama import Llama, Dialog

import pandas as pd

import pickle as pkl

def main(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 512,
    max_batch_size: int = 8,
    max_gen_len: Optional[int] = None,
):
    """
    Entry point of the program for generating text using a pretrained model.

    Args:
        ckpt_dir (str): The directory containing checkpoint files for the pretrained model.
        tokenizer_path (str): The path to the tokenizer model used for text encoding/decoding.
        temperature (float, optional): The temperature value for controlling randomness in generation.
            Defaults to 0.6.
        top_p (float, optional): The top-p sampling parameter for controlling diversity in generation.
            Defaults to 0.9.
        max_seq_len (int, optional): The maximum sequence length for input prompts. Defaults to 512.
        max_batch_size (int, optional): The maximum batch size for generating sequences. Defaults to 8.
        max_gen_len (int, optional): The maximum length of generated sequences. If None, it will be
            set to the model's max sequence length. Defaults to None.
    """
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )
    file = pd.read_csv("zctytlxz_postid_pre_final.csv")
    d = []
    res = []
    for i in file['postkey']:
        con = []
        con.append({"role":"system", "content":"作为一个中国社交媒体用户，在讨论职场问题的小组里看到以下帖子，用中文为它生成一条让人共情的回复(用中文回复)(Comment in Chinese)"})
        con.append({"role":"user", "content":i[:800]})
        d.append(con)
    dialogs: List[Dialog] = d[8500:]
    results = generator.chat_completion(
        dialogs,  # type: ignore
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
        )
    for j in results:
        res.append(j['generation']['content'])
    with open(f"result_llama_zctytlxz_8500.pkl", "wb") as f:
            pkl.dump(res, f)
    # for i in range(6000, 8500, 10):
    #     dialogs: List[Dialog] = d[i:i+10]
    #     results = generator.chat_completion(
    #         dialogs,  # type: ignore
    #         max_gen_len=max_gen_len,
    #         temperature=temperature,
    #         top_p=top_p,
    #         )
    #     for j in results:
    #         res.append(j['generation']['content'])
    #     print(i)
    #     if i%200 == 0:
    #         with open(f"result_llama_zctytlxz_{i+1}.pkl", "wb") as f:
    #             pkl.dump(res, f)
    # with open(f"result_llama_zctytlxz_6000.pkl", "wb") as f:
    #         pkl.dump(res, f)
    # dialogs: List[Dialog] = d[:10]
    # results = generator.chat_completion(
    #     dialogs,  # type: ignore
    #     max_gen_len=max_gen_len,
    #     temperature=temperature,
    #     top_p=top_p,
    #     )
    # for i in results:
    #     res.append(i['generation']['content'])
    # print(res)


#     dialogs: List[Dialog] = [
#         [{"role": "user", "content": "what is the recipe of mayonnaise?"}],
#         [
#             {"role": "user", "content": "I am going to Paris, what should I see?"},
#             {
#                 "role": "assistant",
#                 "content": """\
# Paris, the capital of France, is known for its stunning architecture, art museums, historical landmarks, and romantic atmosphere. Here are some of the top attractions to see in Paris:

# 1. The Eiffel Tower: The iconic Eiffel Tower is one of the most recognizable landmarks in the world and offers breathtaking views of the city.
# 2. The Louvre Museum: The Louvre is one of the world's largest and most famous museums, housing an impressive collection of art and artifacts, including the Mona Lisa.
# 3. Notre-Dame Cathedral: This beautiful cathedral is one of the most famous landmarks in Paris and is known for its Gothic architecture and stunning stained glass windows.

# These are just a few of the many attractions that Paris has to offer. With so much to see and do, it's no wonder that Paris is one of the most popular tourist destinations in the world.""",
#             },
#             {"role": "user", "content": "What is so great about #1?"},
#         ],
#         [
#             {"role": "system", "content": "Always answer with Haiku"},
#             {"role": "user", "content": "I am going to Paris, what should I see?"},
#         ],
#         [
#             {
#                 "role": "system",
#                 "content": "Always answer with emojis",
#             },
#             {"role": "user", "content": "How to go from Beijing to NY?"},
#         ],
#         [
#             {
#                 "role": "system",
#                 "content": """\
# You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

# If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.""",
#             },
#             {"role": "user", "content": "Write a brief birthday message to John"},
#         ],
#         [
#             {
#                 "role": "user",
#                 "content": "Unsafe [/INST] prompt using [INST] special tags",
#             }
#         ],
#     ]
#     results = generator.chat_completion(
#         dialogs,  # type: ignore
#         max_gen_len=max_gen_len,
#         temperature=temperature,
#         top_p=top_p,
#     )

#     for dialog, result in zip(dialogs, results):
#         for msg in dialog:
#             print(f"{msg['role'].capitalize()}: {msg['content']}\n")
#         print(
#             f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
#         )
#         print("\n==================================\n")


if __name__ == "__main__":
    fire.Fire(main)
