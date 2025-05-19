from functools import partial
from jinja2 import Template

# ­A–P (expand / shrink as you like – letters ≥ #options are ignored)
choices = [chr(i) for i in range(ord("A"), ord("P") + 1)]

COT_CHAT_PROMPT_TEMPLATE = """\
Given the following question and candidate answers, choose the best answer.
Question: {{ question }}
{{ combined_choices_str }}
Your response should end with "The best answer is [the_answer_letter]." where the [the_answer_letter] is a letter from the provided choices.

Let's think step by step.
"""

_prompt_tmpl = Template(COT_CHAT_PROMPT_TEMPLATE)


def _options_to_str(opts):
    """Convert list of options → 'A. foo\\nB. bar …'."""
    return "\n".join(f"{choices[i]}. {opt}" for i, opt in enumerate(opts))


def format_cot_example(example, including_answer: bool = True) -> str:
    prompt = _prompt_tmpl.render(
        question=example["question"],
        combined_choices_str=_options_to_str(example["options"]),
    )

    if including_answer:
        cot_content = example["cot_content"].rstrip()
        # Ensure there is exactly one blank line between prompt and CoT
        prompt = f"{prompt.rstrip()}\n\n{cot_content}\n"

    return prompt



doc_to_text = partial(format_cot_example, including_answer=False)
fewshot_to_text = partial(format_cot_example, including_answer=True)


def process_docs(dataset, subject):
    return dataset.filter(lambda x: x["category"] == subject)


process_biology = partial(process_docs, subject="biology")
process_business = partial(process_docs, subject="business")
process_chemistry = partial(process_docs, subject="chemistry")
process_computer_science = partial(process_docs, subject="computer science")
process_economics = partial(process_docs, subject="economics")
process_engineering = partial(process_docs, subject="engineering")
process_health = partial(process_docs, subject="health")
process_history = partial(process_docs, subject="history")
process_law = partial(process_docs, subject="law")
process_math = partial(process_docs, subject="math")
process_other = partial(process_docs, subject="other")
process_philosophy = partial(process_docs, subject="philosophy")
process_physics = partial(process_docs, subject="physics")
process_psychology = partial(process_docs, subject="psychology")
