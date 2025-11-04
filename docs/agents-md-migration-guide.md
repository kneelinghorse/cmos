# agents.md Migration Guide

## Overview

This guide helps you migrate existing CMOS projects to the enhanced memory architecture with agents.md integration. The new system provides better AI agent guidance while maintaining full backward compatibility.

## What's New in Enhanced CMOS

### Key Features
- **agents.md template**: Comprehensive project-specific AI agent configuration
- **Enhanced PROJECT_CONTEXT.json**: New fields for agents.md integration
- **Cross-referencing**: Better context management across multiple files
- **Improved context loading**: Automatic agents.md parsing and validation
- **Backward compatibility**: All existing projects continue to work without changes

## Migration Steps

### Step 1: Add agents.md Template (Recommended)

Copy the agents.md template to your project root:

```bash
cp templates/agents.md ./agents.md
```

Then customize it with your project-specific information:
- Project overview and technology stack
- Build commands and development workflow
- Coding standards and style preferences
- Security guardrails and quality requirements
- Architecture patterns and design decisions

### Step 2: Update PROJECT_CONTEXT.json (Optional)

Add these new fields to your PROJECT_CONTEXT.json:

```json
{
  "working_memory": {
    "agents_md_path": "./agents.md",
    "agents_md_loaded": false,
    "agents_md_version": "1.0.0",
    "active_mission": "",
    "domains": {
      "main": {
        "current_mission": "",
        "missions": {},
        "research_completed": []
      }
    }
  },
  "ai_instructions": {
    "context_priority": [
      "agents.md",
      "PROJECT_CONTEXT.json",
      "MASTER_CONTEXT.json",
      "SESSIONS.jsonl"
    ],
    "special_instructions": [
      "Always read agents.md before starting any mission",
      "Validate agents.md exists and is accessible",
      "Parse agents.md content into working memory",
      "Update agents_md_loaded flag after successful parsing"
    ]
  }
}
```

### Step 3: Validate Your Setup

Verify your migration:

1. Check that agents.md exists in your project root
2. Verify PROJECT_CONTEXT.json has the new fields
3. Test context loading with a simple mission
4. Confirm agents.md is being read by AI agents

## Migration Checklist

- [ ] Copy agents.md template to project root
- [ ] Customize agents.md with project-specific info
- [ ] Update PROJECT_CONTEXT.json with new fields (optional)
- [ ] Test context loading
- [ ] Verify agents.md is accessible
- [ ] Update documentation to reference agents.md

## Backward Compatibility

### Projects Without agents.md
- CMOS continues to work normally
- No breaking changes to existing workflows
- agents.md is completely optional
- All existing missions run unchanged

### Gradual Adoption
You can adopt agents.md features gradually:
1. Start by creating a minimal agents.md
2. Add more sections as needed
3. Update PROJECT_CONTEXT.json when ready
4. No need to update all at once

## Enhanced Features Available After Migration

### For AI Agents
- Project-specific guidance always available
- Better understanding of project structure
- Clear coding standards and preferences
- Security and quality guardrails built-in
- Context loading priority optimized

### For Developers
- Single source of truth for project guidance
- Easier onboarding for new team members
- Better AI agent behavior consistency
- Improved mission success rates
- Clearer development workflows

## Troubleshooting

### agents.md Not Found
**Issue**: AI agent reports agents.md is not accessible

**Solution**:
```bash
# Verify file exists
ls -la agents.md

# Check file permissions
chmod 644 agents.md

# Verify path in PROJECT_CONTEXT.json
cat PROJECT_CONTEXT.json | grep agents_md_path
```

### Context Loading Errors
**Issue**: Context loading fails after migration

**Solution**:
1. Validate JSON syntax in PROJECT_CONTEXT.json
2. Ensure agents.md is valid Markdown
3. Check file paths are correct
4. Revert to backup if needed

### Performance Issues
**Issue**: Context loading is slower after migration

**Solution**:
- Keep agents.md concise (< 500 lines recommended)
- Remove unnecessary sections
- Use compression for large files
- Consider domain-specific agents.md files

## Rollback Procedure

If you need to rollback the migration:

1. **Keep backup copies**:
```bash
cp PROJECT_CONTEXT.json PROJECT_CONTEXT.json.backup
```

2. **Remove new fields** from PROJECT_CONTEXT.json:
   - Remove `agents_md_path`
   - Remove `agents_md_loaded`
   - Remove `agents_md_version`
   - Remove new `ai_instructions` section

3. **Optional**: Remove agents.md file
```bash
mv agents.md agents.md.backup
```

4. **Verify**: Test with existing missions to confirm rollback

## Best Practices

### agents.md Maintenance
- Keep it updated with project changes
- Review quarterly for accuracy
- Version control with Git
- Document major decisions
- Keep sections concise and actionable

### PROJECT_CONTEXT.json Updates
- Set `agents_md_loaded: true` after first successful load
- Update `active_mission` when starting new missions
- Track `research_completed` for dependencies
- Increment `session_count` after each mission

### Integration with Existing Workflows
- Read agents.md at session start
- Reference it during mission execution
- Update it when project standards change
- Use it for onboarding new agents/developers

## Migration Support

### Need Help?
- Review the agents.md template for examples
- Check PROJECT_CONTEXT.json schema documentation
- Test migrations in development environment first
- Keep backups before migrating production projects

### Common Questions

**Q: Is agents.md required?**
A: No, it's optional. CMOS works without it, but agents.md provides better AI agent guidance.

**Q: Can I use a different filename?**
A: Yes, update `agents_md_path` in PROJECT_CONTEXT.json to your custom filename.

**Q: What if my project is multi-language?**
A: Include configuration for all languages in agents.md under language-specific sections.

**Q: How often should I update agents.md?**
A: Update it when project structure, standards, or workflows change significantly.

## Examples

### Minimal agents.md
```markdown
# AI Agent Configuration

## Project Overview
**Project Name**: MyApp
**Primary Language**: JavaScript
**Framework**: React

## Build Commands
```bash
npm install
npm run dev
npm test
```

## Coding Standards
- Use TypeScript
- Follow ESLint rules
- 80% test coverage minimum
```

### Full Migration Example
See `templates/agents.md` for a comprehensive example with all recommended sections.

## Next Steps After Migration

1. **Test the integration**: Run a simple mission to verify agents.md is loaded
2. **Customize agents.md**: Add project-specific guidance
3. **Update documentation**: Reference agents.md in project docs
4. **Train team**: Show developers how to use and maintain agents.md
5. **Monitor effectiveness**: Track improvements in mission success rates

## Version History

- **v1.0.0** (2025-11-02): Initial release with agents.md integration
  - agents.md template
  - Enhanced PROJECT_CONTEXT.json schema
  - Cross-referencing support
  - Backward compatibility maintained

---

**Last Updated**: 2025-11-02
**CMOS Version**: 1.0.0+agents
**Status**: Production Ready
