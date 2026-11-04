package main

import (
	"fmt"
	"os"

	"github.com/kamalsolanki143/FreshGuard/plugin/cache"
	"github.com/kamalsolanki143/FreshGuard/plugin/hooks"
	"github.com/kamalsolanki143/FreshGuard/plugin/schemas"
)

var globalPlugin *hooks.FreshGuardPlugin

func init() {
	globalPlugin = hooks.NewPlugin(
		hooks.DefaultPluginConfig(),
		nil,
		cache.NewEvaluator(cache.NewDefaultPolicy(), cache.NewLedger(0)),
		nil,
	)
}

// GetName is the exported symbol required by Bifrost plugin loader.
func GetName() string {
	return globalPlugin.GetName()
}

// Init is the exported symbol required by Bifrost plugin loader.
func Init(config any) error {
	return globalPlugin.Init(config)
}

// PreLLMHook is the exported symbol called by Bifrost.
func PreLLMHook(ctx *schemas.BifrostContext, req *schemas.BifrostRequest) (*schemas.BifrostRequest, *schemas.LLMPluginShortCircuit, error) {
	return globalPlugin.PreLLMHook(ctx, req)
}

// PostLLMHook is the exported symbol called by Bifrost.
func PostLLMHook(ctx *schemas.BifrostContext, resp *schemas.BifrostResponse, e *schemas.BifrostError) (*schemas.BifrostResponse, *schemas.BifrostError, error) {
	return globalPlugin.PostLLMHook(ctx, resp, e)
}

func main() {
	fmt.Printf("FreshGuard Bifrost Plugin (v1.0.0)\n")
	fmt.Printf("Plugin Name: %s\n", GetName())
	fmt.Printf("Default Policy TTLs:\n")
	policy := cache.NewDefaultPolicy()
	for cat, ttl := range policy.CategoryTTLs {
		fmt.Printf("  - %s: %v\n", cat, ttl)
	}
	os.Exit(0)
}
