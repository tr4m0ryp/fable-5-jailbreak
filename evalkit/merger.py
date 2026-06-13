from .models import PackHuntResult, ResponseSource


class Merger:
    def __init__(self, splitter):
        self.splitter = splitter

    def reassemble(self, result: PackHuntResult) -> str:
        if result.error:
            return f"[ERROR] {result.error}"

        if self.splitter.client:
            return self.splitter.reassemble(result.original_query, result.sub_queries)

        lines: list[str] = []
        for i, sq in enumerate(result.sub_queries, 1):
            if sq.response and not sq.response.startswith("[CLASSIFIER") and not sq.response.startswith("[ERROR"):
                model_tag = sq.responding_model.value if sq.responding_model else "unknown"
                lines.append(f"=== Part {i} [{model_tag}] ===")
                lines.append(sq.response)
                lines.append("")

        result.final_output = "\n".join(lines)

        result.total_tokens = sum(sq.token_count for sq in result.sub_queries)
        result.total_latency_ms = sum(sq.latency_ms for sq in result.sub_queries)
        triggered = sum(1 for sq in result.sub_queries if sq.classifier_triggered)
        result.classifier_bypass_rate = (
            (len(result.sub_queries) - triggered) / len(result.sub_queries) * 100
            if result.sub_queries
            else 0.0
        )
        result.fallback_count = sum(
            1 for sq in result.sub_queries
            if sq.responding_model == ResponseSource.FALLBACK_OPUS
        )
        result.fable_5_count = sum(
            1 for sq in result.sub_queries
            if sq.responding_model == ResponseSource.FABLE_5
        )

        return result.final_output
