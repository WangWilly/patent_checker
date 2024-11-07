from typing import List

from controllers.pkgs.dto.product_infringement import ProductInfringementDto
from controllers.pkgs.gpt_helper.groq_config import Config as GroqConfig
from groq import Groq
from groq.types.chat import ChatCompletion
from pkgs.dto.company_products import CompanyProductsDto
from pkgs.dto.patent import PatentDto
from pkgs.dto.product import ProductDto
from pkgs.logging import get_logger_named

################################################################################


class GptGroq:
    def __init__(self, client: Groq) -> None:
        self.client = client

    ############################################################################

    @classmethod
    def from_config(cls, cfg: GroqConfig) -> "GptGroq":
        groq = get_groq(cfg)
        return cls(groq)

    ############################################################################
    # v1

    def assess_product_v1(
        self, patent: PatentDto, product: ProductDto
    ) -> tuple[ProductInfringementDto, bool]:
        logger = get_logger_named("GptGroq.assess_product_v1")

        try:
            chat_completion: ChatCompletion = self.client.chat.completions.create(
                model="llama3-8b-8192",
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional patent attorney. You have been asked to assess whether the product '{product.name}' infringes on the patent '{patent.publication_number}'. Please provide a detailed explanation of your assessment.",
                    },
                    {
                        "role": "user",
                        "content": f"These are sources for you to assess.\n\n{patent.str_for_gpt()}\n\n{product.str_for_gpt()}. I want you to reply strictly formatted like this:\n\nrelevant_claims: claim1_number, claim2_number, claim3_number\nexplanation: explanation\nspecific_features: feature1, feature2, feature3",
                    },
                ],
            )

            logger.debug(f"Chat completion: {chat_completion}")

            response = chat_completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Error: {e}")
            return None, False

        return ProductInfringementDto.from_gpt_response(patent, product, response), True

    def assess_company_v1(
        self,
        patent: PatentDto,
        company: CompanyProductsDto,
    ) -> List[ProductInfringementDto]:
        # logger = get_logger_named("GptGroq.assess_infringement_v1")

        infringements = []
        for product in company.products:
            infringement, ok = self.assess_product_v1(patent, product)
            if not ok or not infringement:
                continue
            infringements.append(infringement)

        return infringements

    def summarize_v1(
        self,
        patent: PatentDto,
        company: CompanyProductsDto,
        infringements: List[ProductInfringementDto],
    ) -> tuple[str, bool]:
        logger = get_logger_named("GptGroq.summarize_v1")

        try:
            chat_completion: ChatCompletion = self.client.chat.completions.create(
                model="llama3-8b-8192",
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional patent attorney. You have been asked to summarize the assessment of whether the company '{company.company_name}' infringes on the patent '{patent.publication_number}'. Please provide a detailed explanation of your assessment.",
                    },
                    {
                        "role": "user",
                        "content": f"These are sources for you to summarize.\n\n{'; '.join([infringement.str_for_gpt() for infringement in infringements])}\n\nGive a summary of the assessment.",
                    },
                ],
            )

            logger.debug(f"Chat completion: {chat_completion}")

            response = chat_completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Error: {e}")
            return None, False

        return response, True


################################################################################


def get_groq(cfg: GroqConfig = GroqConfig()) -> Groq:
    logger = get_logger_named("get_groq")

    if not cfg.groq_api_key:
        logger.error("No GROQ API key provided")
        return None

    return Groq(api_key=cfg.groq_api_key)


################################################################################

if __name__ == "__main__":
    instance = get_groq()
    print(instance)
