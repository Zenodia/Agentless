from datasets import load_dataset
from agentless.fl.localize import localize_instance
from agentless.util.preprocess_data import (
    check_contains_valid_loc,
    filter_none_python,
    filter_out_test_files,
    get_repo_structure,
)

from get_repo_structure.get_repo_structure import (
    get_project_structure_from_scratch,
    parse_python_file,
)

from agentless.util.preprocess_data import (
    check_contains_valid_loc,
    filter_none_python,
    filter_out_test_files,
    get_repo_structure,
)

from agentless.fl.FL import LLMFL
from agentless.util.utils import load_existing_instance_ids, load_jsonl, setup_logger

swe_bench_data = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")
sample=swe_bench_data[0]

start_file_locs = None
existing_instance_ids = set()
d = get_project_structure_from_scratch(
            sample["repo"], sample["base_commit"], sample["instance_id"], "playground"
        )
structure = d["structure"]
instance_id=sample["instance_id"]

#logger.info(f"================ localize {instance_id} ================")

bench_data = [x for x in swe_bench_data if x["instance_id"] == instance_id][0]
problem_statement = bench_data["problem_statement"]

filter_none_python(structure)  # some basic filtering steps
filter_out_test_files(structure)

logger = setup_logger('logger.log')

found_files = []
found_related_locs = {}
found_edit_locs = {}
additional_artifact_loc_file = None
additional_artifact_loc_related = None
additional_artifact_loc_edit_location = None
file_traj, related_loc_trajs, edit_loc_traj = {}, [], {}

file_level=True

fl=LLMFL(instance_id,structure,problem_statement, "nvdev/meta/llama-3.1-405b-instruct", 'nvidia', logger)
found_files, additional_artifact_loc_file, file_traj = fl.localize_irrelevant(mock=False)
print(found_files)
print("---*10")
print("\n\n\n")
print(additional_artifact_loc_file)
print("---*10")
print("\n\n\n")
print(file_traj)