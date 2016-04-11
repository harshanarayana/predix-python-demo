from flask import Flask, request
from nameko.standalone.rpc import ServiceRpcProxy

app = Flask(__name__)


@app.route('/')
def task_list():
    return """
        <html>
            <body>
                <h1>Available Tasks</h1>
                <h2>Fibonacci</h2>
                <form action="/fibonacci" method="post">
                    Number:
                    <input type="text" name="n">
                    <input type="submit" value="Submit">
                </form>
            </body>
        </html>
    """


@app.route('/fibonacci', methods=['POST'])
def start_task():
    n = int(request.form['n'])
    with rpc_proxy() as task_proxy:
        task_id = task_proxy.start_task("fibonacci", n)

    return """
        <html>
            <body>
                <p>
                    Your task is running.
                    <a href="/task/{task_id}">Result</a>
                </p>
            </body>
        </html>
    """.format(task_id=task_id)


@app.route('/task/<string:task_id>')
def task_result(task_id):
    with rpc_proxy() as task_proxy:
        result = task_proxy.get_result(task_id)

    return """
        <html>
            <body>
                <p>The result of task {task_id} is {result}.</p>
            </body>
        </html>
    """.format(task_id=task_id, result=result)


def rpc_proxy():
    # the ServiceRpcProxy instance isn't thread safe so we constuct one for
    # each request; a more intelligent solution would be a thread-local or
    # pool of shared proxies
    config = {'AMQP_URI': 'amqp://guest:guest@localhost/'}
    return ServiceRpcProxy('tasks', config)


if __name__ == '__main__':
    app.run(debug=True)
