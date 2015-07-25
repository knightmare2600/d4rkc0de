Code:
<?php
function xml2array($elements_string)
{
    $xml_array = array();
    $elements_regex = '/<(\w+)\s*([^\/>]*)\s*(?:\/>|>(.*?)<(\/\s*\1\s*)>)/s';
    $attributes_regex = '/(\w+)=(?:"|\')([^"\']*)(:?"|\')/';
    preg_match_all ($elements_regex, $elements_string, $elements_array);
    foreach ( $elements_array[1] as $e_key => $e_value )
    {
        $xml_array[$e_key]["name"] = $e_value;
        if ( ($attributes_string = trim($elements_array[2][$e_key])) )
        {
            preg_match_all($attributes_regex, $attributes_string, $attributes_array);
            foreach ( $attributes_array[1] as $a_key => $a_value )
            {
                $xml_array[$a_key]["attributes"][$a_value] = $attributes_array[2][$a_key];
            }
        }
        if ( ($p = strpos($elements_array[3][$e_key], "<")) > 0 )
        {
            $xml_array[$e_key]["text"] = substr($elements_array[3][$e_key], 0, $p - 1);
        }
        if ( preg_match($elements_regex, $elements_array[3][$e_key]) )
        {       
            $xml_array[$e_key]["elements"] = xml2array($elements_array[3][$e_key]);
        }
        else if ( isset($elements_array[3][$e_key]) )
        {
            $xml_array[$e_key]["text"] = $elements_array[3][$e_key];
        }
        $xml_array[$e_key]["closetag"] = $elements_array[4][$e_key];
    }
    return $xml_array;
}
$xml = xml2array(file_get_contents("./news.xml"));
print_r($xml);
?>