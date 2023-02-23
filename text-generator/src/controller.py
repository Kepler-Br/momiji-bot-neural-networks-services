import threading
from concurrent.futures import ThreadPoolExecutor, Future
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from starlette import status

from dto import GenerateTextRequest
from language_neural_network_abstract import LanguageNeuralNetworkAbstract


class Controller:
    def __init__(self, network: LanguageNeuralNetworkAbstract):
        self._network = network
        self._network_lock = threading.RLock()
        self._tasks_lock = threading.RLock()
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._tasks: dict[UUID, Future] = dict()

        self.router = APIRouter()

        self.router.add_api_route('/generated-text/{task_key}', self.request_generation, methods=['POST'])
        self.router.add_api_route('/generated-text/{task_key}', self.get_generation, methods=['GET'])

    def _generate(self, body: GenerateTextRequest) -> list[str]:
        with self._network_lock:
            return self._network.generate(
                prompt=body.prompt,
                count=body.count,
                max_new_tokens=body.max_new_tokens,
                num_beams=body.num_beams,
                no_repeat_ngram_size=body.no_repeat_ngram_size,
                early_stopping=body.early_stopping,
                seed=body.seed,
                bad_words=body.bad_words,
                top_k=body.top_k,
                top_p=body.top_p,
                temperature=body.temperature,
                repetition_penalty=body.repetition_penalty,
            )

    def get_generation(self, task_key: UUID) -> Response:
        if task_key not in self._tasks:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        task = self._tasks[task_key]

        if not task.done():
            return Response(status_code=status.HTTP_425_TOO_EARLY)

        result = task.result()

        self._tasks.pop(task_key)

        return JSONResponse(
            content={
                'result': result
            }
        )

    def request_generation(self, body: GenerateTextRequest, task_key: UUID) -> Response:
        if task_key not in self._tasks:
            self._tasks[task_key] = self._executor.submit(self._generate, body)

        return Response(
            status_code=status.HTTP_201_CREATED
        )
