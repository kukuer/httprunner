# NOTE: Generated By HttpRunner v3.0.11
# FROM: examples/httpbin/hooks.yml

from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


class TestCaseHooks(HttpRunner):
    config = Config("basic test with httpbin").base_url("${get_httpbin_server()}")

    teststeps = [
        Step(
            RunRequest("headers")
            .with_variables(**{"a": 123})
            .setup_hook("${setup_hook_add_kwargs($request)}")
            .setup_hook("${setup_hook_remove_kwargs($request)}")
            .get("/headers")
            .teardown_hook("${teardown_hook_sleep_N_secs($response, 1)}")
            .validate()
            .assert_equal("status_code", 200)
            .assert_contained_by("body.headers.Host", "${get_httpbin_server()}")
        ),
        Step(
            RunRequest("alter response")
            .get("/headers")
            .teardown_hook("${alter_response($response)}")
            .validate()
            .assert_equal("status_code", 500)
            .assert_equal('headers."Content-Type"', "html/text")
            .assert_equal('body.headers."Content-Type"', "application/json")
            .assert_equal("body.headers.Host", "127.0.0.1:8888")
        ),
    ]


if __name__ == "__main__":
    TestCaseHooks().test_start()
