# TestRail API Modules Quick Reference

All modules are accessed as properties on the `api` object: `api.{module}.{method}(...)`.
All methods use keyword arguments. Return types are `dict` or `list[dict]`.

## Table of Contents

- [attachments](#apiattachments)
- [bdd](#apibdd)
- [cases](#apicases)
- [configurations](#apiconfigurations)
- [datasets](#apidatasets)
- [groups](#apigroups)
- [milestones](#apimilestones)
- [plans](#apiplans)
- [priorities](#apipriorities)
- [projects](#apiprojects)
- [reports](#apireports)
- [result_fields](#apiresult_fields)
- [results](#apiresults)
- [roles](#apiroles)
- [runs](#apiruns)
- [sections](#apisections)
- [shared_steps](#apishared_steps)
- [statuses](#apistatuses)
- [suites](#apisuites)
- [templates](#apitemplates)
- [tests](#apitests)
- [users](#apiusers)
- [variables](#apivariables)

## api.attachments

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_attachment(entity_type, entity_id, file_path)` | entity_type, entity_id, file_path | Upload attachment |
| `delete_attachment(attachment_id)` | attachment_id | Delete attachment |
| `get_attachment(attachment_id)` | attachment_id | Get attachment metadata |
| `get_attachment_content(attachment_id)` | attachment_id | Download attachment content |
| `get_attachments(entity_type, entity_id)` | entity_type, entity_id | List attachments |

Entity types: `"case"`, `"run"`, `"plan"`, `"result"`, `"test"`

## api.bdd

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_bdd(section_id, feature_file)` | section_id, feature_file | Import BDD feature file |
| `get_bdd(case_id)` | case_id | Export BDD scenario |

## api.cases

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_case(section_id, title, ...)` | section_id, title | Create test case |
| `clear_case_fields_cache()` | (none) | Clear cached field definitions |
| `copy_cases_to_section(case_ids, section_id)` | case_ids, section_id | Copy cases |
| `delete_case(case_id)` | case_id | Delete test case |
| `get_case(case_id)` | case_id | Get single case |
| `get_case_fields()` | (none) | Get all field definitions |
| `get_case_history(case_id)` | case_id | Get change history |
| `get_case_types()` | (none) | Get available case types |
| `get_cases(project_id, ...)` | project_id | List cases (filter by suite_id, section_id) |
| `get_field_options(field_name)` | field_name | Get dropdown/multi-select options |
| `get_required_case_fields(...)` | (section_id recommended) | Get required fields with format hints |
| `move_cases_to_section(case_ids, section_id)` | case_ids, section_id | Move cases |
| `update_case(case_id, ...)` | case_id | Update test case |

Optional params for `add_case`/`update_case`: `type_id`, `priority_id`, `estimate`, `milestone_id`, `refs`, `description`, `preconditions`, `postconditions`, `custom_fields`

## api.configurations

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_configuration(project_id, name)` | project_id, name | Create configuration |
| `delete_configuration(config_id)` | config_id | Delete configuration |
| `get_configuration(config_id)` | config_id | Get configuration |
| `get_configurations(project_id)` | project_id | List configurations |
| `update_configuration(config_id, **kwargs)` | config_id | Update configuration |

## api.datasets

| Method | Required Params | Description |
|--------|----------------|-------------|
| `get_dataset(dataset_id)` | dataset_id | Get dataset |
| `get_datasets(project_id)` | project_id | List datasets |

## api.groups

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_group(project_id, name)` | project_id, name | Create group |
| `add_group_to_suite(group_id, suite_id)` | group_id, suite_id | Associate group with suite |
| `delete_group(group_id)` | group_id | Delete group |
| `get_group(group_id)` | group_id | Get group |
| `get_group_cases(group_id)` | group_id | Get cases in group |
| `get_group_suites(group_id)` | group_id | Get suites for group |
| `get_groups(project_id)` | project_id | List groups |
| `remove_group_from_suite(group_id, suite_id)` | group_id, suite_id | Disassociate group from suite |
| `update_group(group_id)` | group_id | Update group |

## api.milestones

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_milestone(project_id, name)` | project_id, name | Create milestone |
| `delete_milestone(milestone_id)` | milestone_id | Delete milestone |
| `get_milestone(milestone_id)` | milestone_id | Get milestone |
| `get_milestone_stats(milestone_id)` | milestone_id | Get milestone statistics |
| `get_milestones(project_id)` | project_id | List milestones |
| `update_milestone(milestone_id)` | milestone_id | Update milestone |

## api.plans

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_plan(project_id, name)` | project_id, name | Create test plan |
| `close_plan(plan_id)` | plan_id | Close test plan |
| `delete_plan(plan_id)` | plan_id | Delete test plan |
| `get_plan(plan_id)` | plan_id | Get plan with entries |
| `get_plan_stats(plan_id)` | plan_id | Get plan statistics |
| `get_plans(project_id)` | project_id | List plans |
| `update_plan(plan_id)` | plan_id | Update plan / add entries |

## api.priorities

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_priority(name, short_name, color)` | name, short_name, color | Create priority |
| `delete_priority(priority_id)` | priority_id | Delete priority |
| `get_priorities()` | (none) | List all priorities |
| `get_priority(priority_id)` | priority_id | Get priority |
| `get_priority_counts(project_id)` | project_id | Get priority distribution |
| `get_priority_stats(project_id)` | project_id | Get priority statistics |
| `update_priority(priority_id)` | priority_id | Update priority |

## api.projects

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_project(name)` | name | Create project |
| `add_project_attachment(project_id, file_path)` | project_id, file_path | Upload project attachment |
| `delete_project(project_id)` | project_id | Delete project |
| `get_project(project_id)` | project_id | Get project details |
| `get_project_activity(project_id)` | project_id | Get activity log |
| `get_project_attachments(project_id)` | project_id | List project attachments |
| `get_project_stats(project_id)` | project_id | Get project statistics |
| `get_projects()` | (none) | List all projects |
| `update_project(project_id)` | project_id | Update project |

## api.reports

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_report(project_id, name)` | project_id, name | Create report |
| `delete_report(report_id)` | report_id | Delete report |
| `get_report(report_id)` | report_id | Get report |
| `get_report_results(report_id)` | report_id | Get report results |
| `get_reports(project_id)` | project_id | List reports |
| `run_report(report_id)` | report_id | Execute report |
| `update_report(report_id)` | report_id | Update report |

## api.result_fields

| Method | Required Params | Description |
|--------|----------------|-------------|
| `get_result_field(field_id)` | field_id | Get result field definition |
| `get_result_fields()` | (none) | List all result field definitions |

## api.results

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_result(run_id, case_id, status_id)` | run_id, case_id, status_id | Record single result |
| `add_result_for_run(run_id, status_id)` | run_id, status_id | Add result for run |
| `add_results(run_id, results)` | run_id, results | Batch add results |
| `add_results_for_cases(run_id, results)` | run_id, results | Batch add results by case_id |
| `get_results(run_id)` | run_id | Get results |
| `get_results_for_case(run_id, case_id)` | run_id, case_id | Get results for specific case |
| `get_results_for_run(run_id)` | run_id | Get all results for a run |

Optional params for `add_result`: `comment`, `version`, `elapsed`, `defects`

## api.roles

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_role(name)` | name | Create role |
| `delete_role(role_id)` | role_id | Delete role |
| `get_role(role_id)` | role_id | Get role |
| `get_roles()` | (none) | List all roles |
| `update_role(role_id, **kwargs)` | role_id | Update role |

## api.runs

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_run(project_id, name)` | project_id, name | Create test run |
| `close_run(run_id)` | run_id | Close test run |
| `delete_run(run_id)` | run_id | Delete test run |
| `get_run(run_id)` | run_id | Get run details |
| `get_run_stats(run_id)` | run_id | Get run statistics |
| `get_runs(project_id)` | project_id | List runs |
| `update_run(run_id)` | run_id | Update run |

Optional params for `add_run`: `suite_id`, `description`, `milestone_id`, `include_all`, `case_ids`

## api.sections

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_section(project_id, name)` | project_id, name | Create section |
| `delete_section(section_id)` | section_id | Delete section |
| `get_section(section_id)` | section_id | Get section |
| `get_section_cases(section_id)` | section_id | Get cases in section |
| `get_section_stats(section_id)` | section_id | Get section statistics |
| `get_sections(project_id)` | project_id | List sections (optional: suite_id) |
| `update_section(section_id)` | section_id | Update section |

## api.shared_steps

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_shared_step(project_id, title, steps)` | project_id, title, steps | Create shared step |
| `delete_shared_step(shared_step_id)` | shared_step_id | Delete shared step |
| `get_shared_step(shared_step_id)` | shared_step_id | Get shared step |
| `get_shared_steps(project_id)` | project_id | List shared steps |
| `update_shared_step(shared_step_id, **kwargs)` | shared_step_id | Update shared step |

## api.statuses

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_status(name, short_name, color)` | name, short_name, color | Create status |
| `delete_status(status_id)` | status_id | Delete status |
| `get_status(status_id)` | status_id | Get status |
| `get_status_counts(run_id)` | run_id | Get result counts by status |
| `get_status_history(result_id)` | result_id | Get status change history |
| `get_statuses()` | (none) | List all statuses |
| `update_status(status_id)` | status_id | Update status |

## api.suites

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_suite(project_id, name)` | project_id, name | Create suite |
| `delete_suite(suite_id)` | suite_id | Delete suite |
| `get_suite(suite_id)` | suite_id | Get suite |
| `get_suite_cases(suite_id)` | suite_id | Get cases in suite |
| `get_suite_runs(suite_id)` | suite_id | Get runs for suite |
| `get_suite_stats(suite_id)` | suite_id | Get suite statistics |
| `get_suites(project_id)` | project_id | List suites |
| `update_suite(suite_id)` | suite_id | Update suite |

## api.templates

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_template(project_id, name)` | project_id, name | Create template |
| `add_template_field(template_id, name, field_type)` | template_id, name, field_type | Add field to template |
| `delete_template(template_id)` | template_id | Delete template |
| `delete_template_field(template_id, field_id)` | template_id, field_id | Remove field from template |
| `get_template(template_id)` | template_id | Get template |
| `get_template_fields(template_id)` | template_id | Get template fields |
| `get_templates(project_id)` | project_id | List templates |
| `update_template(template_id)` | template_id | Update template |
| `update_template_field(template_id, field_id)` | template_id, field_id | Update template field |

## api.tests

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_test_result(test_id, status_id)` | test_id, status_id | Add result to test |
| `add_test_results(test_ids, results)` | test_ids, results | Batch add test results |
| `get_test(test_id)` | test_id | Get test |
| `get_test_results(test_id)` | test_id | Get results for test |
| `get_tests(run_id)` | run_id | List tests in a run |

## api.users

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_user(name, email, password)` | name, email, password | Create user |
| `delete_user(user_id)` | user_id | Delete user |
| `get_user(user_id)` | user_id | Get user |
| `get_user_activity(user_id)` | user_id | Get user activity log |
| `get_user_by_email(email)` | email | Find user by email |
| `get_user_projects(user_id)` | user_id | Get user's projects |
| `get_user_roles(user_id)` | user_id | Get user's roles |
| `get_users()` | (none) | List all users |
| `update_user(user_id)` | user_id | Update user |

## api.variables

| Method | Required Params | Description |
|--------|----------------|-------------|
| `add_variable(project_id, name, value)` | project_id, name, value | Create variable |
| `add_variable_group(project_id, name)` | project_id, name | Create variable group |
| `delete_variable(variable_id)` | variable_id | Delete variable |
| `delete_variable_group(group_id)` | group_id | Delete variable group |
| `get_variable(variable_id)` | variable_id | Get variable |
| `get_variable_groups(project_id)` | project_id | Get variable groups |
| `get_variables(project_id)` | project_id | List variables |
| `update_variable(variable_id)` | variable_id | Update variable |
| `update_variable_group(group_id)` | group_id | Update variable group |
