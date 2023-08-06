function GetOciTopLevelCommand_instance_agent() {
    return 'instance-agent'
}

function GetOciSubcommands_instance_agent() {
    $ociSubcommands = @{
        'instance-agent' = 'command command-execution'
        'instance-agent command' = 'cancel create get list'
        'instance-agent command-execution' = 'get list'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_instance_agent() {
    $ociCommandsToLongParams = @{
        'instance-agent command cancel' = 'command-id force from-json help if-match'
        'instance-agent command create' = 'compartment-id content display-name from-json help target timeout-in-seconds'
        'instance-agent command get' = 'command-id from-json help'
        'instance-agent command list' = 'all compartment-id from-json help limit page page-size sort-by sort-order'
        'instance-agent command-execution get' = 'command-id from-json help instance-id'
        'instance-agent command-execution list' = 'all compartment-id from-json help instance-id lifecycle-state limit page page-size sort-by sort-order'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_instance_agent() {
    $ociCommandsToShortParams = @{
        'instance-agent command cancel' = '? h'
        'instance-agent command create' = '? c h'
        'instance-agent command get' = '? h'
        'instance-agent command list' = '? c h'
        'instance-agent command-execution get' = '? h'
        'instance-agent command-execution list' = '? c h'
    }
    return $ociCommandsToShortParams
}