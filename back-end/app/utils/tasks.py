import time


def test_rq(num):
    print('Starting task')
    for i in range(num):
        print(i)
        time.sleep(1)
    print('Task completed')
    return 'Done'
