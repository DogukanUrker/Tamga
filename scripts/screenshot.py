from tamga import Tamga

logger = Tamga(
    showTime=True,
    showTimezone=False,
    isColored=True,
    logToConsole=True,
)

print("\n")

logger.info("🤖 AI assistant online — ready to help!")
logger.success("🎉 User onboarding complete: @dogi_rocks")
logger.warning("⚡️ API rate limit approaching (90%)")
logger.error("💥 Payment failed: Card declined")
logger.critical("🚨 Data breach detected! Initiating lockdown")
logger.debug("🔍 Feature flag 'beta_mode' is ON")
logger.custom("🛒 Checkout event: Cart abandoned", "METRIC", "cyan")
logger.custom("🎨 Theme switched to 'dark mode'", "UI", "purple")
logger.dir(
    "🔑 User login",
    user_id="42",
    verified=True,
)
logger.info("🌈 All systems go. Have an epic day!")

print("\n")
