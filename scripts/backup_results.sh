#!/bin/bash
# Backup hyperopt results with timestamp

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="backups/hyperopt_backup_$TIMESTAMP"

echo "💾 Creating backup: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# Backup output directory
if [ -d "output" ]; then
    cp -r output "$BACKUP_DIR/"
    echo "✅ Backed up output directory"
fi

# Backup logs
if [ -d "logs" ]; then
    cp -r logs "$BACKUP_DIR/"
    echo "✅ Backed up logs directory"
fi

# Backup configs
if [ -d "configs" ]; then
    cp -r configs "$BACKUP_DIR/"
    echo "✅ Backed up configs directory"
fi

echo "🎉 Backup completed: $BACKUP_DIR"
