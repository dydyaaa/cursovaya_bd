import asyncio
import httpx
import time
import threading

async def make_request(client, url):
    try:
        response = await client.get(url)
        return response
    except httpx.RequestError:
        return None

async def test_api_performance(url, num_users, test_duration):
    total_requests = 0
    successful_requests = 0
    error_5xx_requests = 0
    total_response_time = 0
    total_requests_lock = threading.Lock()

    start_time = time.time()

    async def request_worker(client):
        nonlocal total_requests, successful_requests, error_5xx_requests, total_response_time
        while time.time() - start_time < test_duration:
            response = await make_request(client, url)
            with total_requests_lock:
                total_requests += 1
                if response:
                    total_response_time += response.elapsed.total_seconds()
                    if response.status_code == 200:
                        successful_requests += 1
                    elif response.status_code >= 500:
                        error_5xx_requests += 1

    def log_progress():
        nonlocal total_requests
        while time.time() - start_time < test_duration:
            with total_requests_lock:
                print(f"Прошло {int(time.time() - start_time)} секунд, общее количество запросов: {total_requests}")
            time.sleep(1)

    # Логирование в отдельном потоке
    log_thread = threading.Thread(target=log_progress)
    log_thread.start()

    async with httpx.AsyncClient() as client:
        tasks = [asyncio.create_task(request_worker(client)) for _ in range(num_users)]
        await asyncio.gather(*tasks)

    log_thread.join()

    total_time = time.time() - start_time
    avg_response_time = total_response_time / successful_requests if successful_requests > 0 else float('inf')
    rps = total_requests / total_time if total_time > 0 else 0
    error_5xx_percentage = (error_5xx_requests / total_requests) * 100 if total_requests > 0 else 0

    print(f"Среднее время ответа: {avg_response_time:.3f} секунд")
    print(f"Запросов в секунду (RPS): {rps:.1f}")
    print(f"Процент запросов с ошибкой 5xx: {error_5xx_percentage:.2f}%")

# Пример использования:
if __name__ == "__main__":
    url = "https://sogazik.ru/"
    num_users = 200
    test_duration = 50

    asyncio.run(test_api_performance(url, num_users, test_duration))
