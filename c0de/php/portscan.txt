code:  <?php

set_time_limit(0);
error_reporting(0);

echo "PHP Portscanner by TheMagician.\n\n";

if($argc == 3)
{
  if(strpos($argv[2], "-"))
  {
    $ports = explode("-", $argv[2]);
  }
  else
  {
    $port = $argv[2];
  }
  $host = $argv[1];
}
else
{
  echo "Syntax: php $argv[0] 127.0.0.1 1-65535\n";
  exit;
}

while(true)
{
  if(isset($ports))
  {
    if($ports[0] < 1)
    {
      $start = 1;
    }
    else
    {
      $start = $ports[0];
    }
    if($ports[1] > 65535)
    {
      $end = 65535;
    }
    else
    {
      $end = $ports[1];
    }

    for($start; $start <= $end; $start++)
    {
      $sock = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
      if(socket_connect($sock, $host, $start))
      {
        echo "Port $start is open.\n";
        socket_close($sock);
      }
      else
      {
        echo "Port $start is not open.\n";
        socket_close($sock);
      }
    }
    break;
  }
  else
  {
    $sock = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    if(socket_connect($sock, $host, $port))
    {
      echo "Port $port is open.\n";
      socket_close($sock);
    }
    else
    {
      echo "Port $port is not open.\n";
      socket_close($sock);
    }
    break;
  }
}

?>