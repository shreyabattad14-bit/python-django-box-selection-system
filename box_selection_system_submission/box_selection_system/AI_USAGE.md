# AI_USAGE.md

## AI tool used

ChatGPT was used as an AI coding assistant during preparation of this assignment.

## Prompts used

The main request was to build a small Django/Python box-selection system from the supplied hiring-assignment specification and prepare the requested repository deliverables.

Follow-up prompts were used to:
- clarify the assignment requirements;
- design Django models and the recommendation rule;
- create and review tests;
- prepare README and AI-usage documentation;
- run and verify the test suite.

## Accepted output

The generated project structure, model/API/test scaffolding, and documentation were reviewed and adapted to the assignment requirements.

## Rejected or modified output

The solution was intentionally constrained to a simple, deterministic single-box recommendation rule rather than pretending to solve exact multi-item 3-D packing. The README documents this limitation.

## Mistakes / risks identified

- Exact multi-item 3-D packing is not guaranteed by a volume-only check.
- Therefore, the implementation also requires every individual product to fit inside the candidate box under some rotation.
- API validation was added for malformed JSON, missing fields, non-positive dimensions/weights, and invalid quantity values.

## Verification steps

1. Installed dependencies from `requirements.txt`.
2. Ran Django migrations.
3. Ran the automated test suite with `python manage.py test`.
4. Reviewed the recommendation and API tests.
5. Confirmed that the final test run completed successfully; see `TEST_OUTPUT.md`.

## Important note

The hiring assignment asks the candidate to include an exported chat transcript and to explain what they personally learned without using AI to generate that response. The actual chat transcript should be exported from the AI interface used by the candidate and placed in the repository. The candidate should also write the personal-learning response in their own words.
