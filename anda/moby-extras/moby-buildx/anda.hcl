project "pkg" {
    rpm {
        spec = "moby-buildx.spec"
        sources = "."
    }
}