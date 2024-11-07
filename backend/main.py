from argparse import ArgumentParser

import uvicorn
from controllers.gpt.config import Config as GptCtrlConfig
from controllers.gpt.controller import Controller as GptController
from controllers.infringement.config import Config as InfringementCtrlConfig
from controllers.infringement.controller import \
    Controller as InfringementController
from controllers.pkgs.gpt_helper.groq import GptGroq
from controllers.pkgs.gpt_helper.groq_config import Config as GroqConfig
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pkgs.db_helper.config import Config as DbConfig
from pkgs.db_helper.postgresql import get_db
from pkgs.logging import get_logger_named, set_default_level

################################################################################


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to run the server on"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to run the server on"
    )
    parser.add_argument(
        "--workers", type=int, default=1, help="Number of worker processes"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Run the server in debug mode"
    )

    args = parser.parse_args()

    ############################################################################

    # Initialize logger
    set_default_level(args.debug)  # TODO: plan to remove this
    logger = get_logger_named("main")

    ############################################################################

    # Initialize FastAPI app
    app = FastAPI()

    ############################################################################
    # Cors

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    ############################################################################
    # Helper
    groq_cfg = GroqConfig()
    gptHelper: GptGroq = GptGroq.from_config(groq_cfg)

    db_cfg = DbConfig()
    db = get_db(db_cfg)

    ############################################################################
    # Initialize controllers

    gpt_ctrl_cfg = GptCtrlConfig()
    gpt_controller = GptController(gpt_ctrl_cfg, gptHelper)
    app.include_router(gpt_controller.get_router())

    infringement_ctrl_cfg = InfringementCtrlConfig()
    infringement_controller = InfringementController(db, infringement_ctrl_cfg)
    app.include_router(infringement_controller.get_router())

    ############################################################################

    # Start the server
    logger.info(
        f"Starting server on {args.host}:{args.port} with {args.workers} workers"
    )
    uvicorn.run(app, host=args.host, port=args.port, workers=args.workers)

    db.close()
    logger.info("Server stopped")


################################################################################

if __name__ == "__main__":
    main()
