from typing import Tuple


def changeBackgroundAnimation(animationSpeed: int = 40) -> None: ...


def checkForQuit() -> None: ...


def drawButtons() -> None: ...


def flashButtonAnimation(color: Tuple[int, int, int], animationSpeed: int = 50) -> None: ...


def gameOverAnimation(color: Tuple[int, int, int] = (255, 255, 255), animationSpeed: int = 50) -> None: ...


def getButtonClicked(x: int, y: int) -> Tuple[int, int, int]: ...


def main() -> None: ...


def terminate() -> None: ...
