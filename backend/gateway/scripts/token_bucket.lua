local key = KEYS[1]

local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

local bucket = redis.call("HMGET", key, "tokens", "last_refill")

local tokens = tonumber(bucket[1])
local last_refill = tonumber(bucket[2])

if not tokens then
    tokens = capacity
    last_refill = now
end

local elapsed = now - last_refill

local refill_amount = elapsed * refill_rate

tokens = math.min(
    capacity,
    tokens + refill_amount
)

if tokens < 1 then
    local retry_after = math.ceil((1 - tokens) / refill_rate)

    redis.call(
        "HMSET",
        key,
        "tokens", tokens,
        "last_refill", now
    )

    redis.call("EXPIRE", key, 3600)

    return {0, tokens, retry_after}
end

tokens = tokens - 1

redis.call(
    "HMSET",
    key,
    "tokens", tokens,
    "last_refill", now
)

redis.call("EXPIRE", key, 3600)

return {1, tokens, 0}