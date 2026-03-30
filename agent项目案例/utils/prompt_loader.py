from agent项目案例.utils.log_tool import logger
from agent项目案例.utils.path_tool import get_abs_path
from agent项目案例.utils.config_handler import prompt_conf


def load_system_prompts():
    try:
        system_prompt_path = get_abs_path(prompt_conf["main_prompt_path"])
    except KeyError as e:
        raise Exception(f"请检查配置文件 {get_abs_path('config/prompts.yml')} 是否正确") from e
    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"读取系统提示提示词{system_prompt_path} 失败", exc_info=True)
        raise e

def load_rag_prompts():
    try:
        rag_summarize_prompt_path = get_abs_path(prompt_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        raise Exception(f"请检查配置文件 {get_abs_path('config/rag.yml')} 是否正确") from e
    try:
        return open(rag_summarize_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"读取系统提示提示词{rag_summarize_prompt_path} 失败", exc_info=True)
        raise e


def load_report_prompts():
    try:
        report_prompt_path = get_abs_path(prompt_conf["report_prompt_path"])
    except KeyError as e:
        raise Exception(f"请检查配置文件 {get_abs_path('config/report.yml')} 是否正确") from e
    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"读取系统提示提示词{report_prompt_path} 失败", exc_info=True)
        raise e

if __name__ == '__main__':
    # print(load_system_prompts())
    print(load_rag_prompts())
    print(load_report_prompts())
